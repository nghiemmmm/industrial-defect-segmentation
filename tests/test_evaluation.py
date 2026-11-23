import os
import shutil
import tempfile
import pytest
import numpy as np

from evaluation.dual_domain_metrics import (
    masks_to_anomaly_map,
    compute_mask_iou,
    compute_pixel_auroc,
    compute_image_auroc,
    compute_false_alarm_rate,
    DualDomainEvaluator,
)
from evaluation.robustness_evaluator import RobustnessEvaluator
from experiments.ablation_matrix import collect_ablation_results


class TestDualDomainMetrics:
    def test_perfect_predictions(self):
        """
        Perfect prediction scenario:
        Model predicts identical masks with confidence 0.99 for defects,
        and zero detection (confidence 0.0) for good parts.
        Expected: IoU == 1.0, Pixel-AUROC == 1.0, Image-AUROC == 1.0, FAR == 0.0.
        """
        h, w = 64, 64
        # 3 defective images
        gt_masks = []
        pred_maps = []
        for i in range(3):
            gt = np.zeros((h, w), dtype=np.uint8)
            gt[10:30, 10:30] = 255
            gt_masks.append(gt)

            # Reconstruct anomaly map from exact mask with conf=0.99
            p_map = masks_to_anomaly_map([gt], [0.99], (h, w))
            pred_maps.append(p_map)

        defect_confs = [0.99, 0.99, 0.99]
        good_confs = [0.0, 0.0, 0.0]  # clean good parts

        # 1. IoU
        for gt, pr in zip(gt_masks, pred_maps):
            iou = compute_mask_iou((pr >= 0.5).astype(np.uint8) * 255, gt)
            assert pytest.approx(iou, 1e-4) == 1.0

        # 2. Pixel-AUROC
        # Add normal images with all-zero GT and all-zero pred
        all_gt = gt_masks + [np.zeros((h, w), dtype=np.uint8) for _ in good_confs]
        all_pred = pred_maps + [np.zeros((h, w), dtype=np.float32) for _ in good_confs]
        px_auroc = compute_pixel_auroc(all_gt, all_pred)
        assert pytest.approx(px_auroc, 1e-4) == 1.0

        # 3. Image-AUROC
        gt_is_anomaly = [1, 1, 1, 0, 0, 0]
        sp_confs = defect_confs + good_confs
        img_auroc = compute_image_auroc(gt_is_anomaly, sp_confs)
        assert pytest.approx(img_auroc, 1e-4) == 1.0

        # 4. False Alarm Rate
        far_025 = compute_false_alarm_rate(good_confs, conf_threshold=0.25)
        far_050 = compute_false_alarm_rate(good_confs, conf_threshold=0.50)
        assert far_025 == 0.0
        assert far_050 == 0.0

    def test_inverted_and_imperfect_predictions(self):
        """
        Inverted prediction scenario:
        High probability on normal background, zero on defect.
        Expected: Pixel-AUROC == 0.0.
        """
        h, w = 32, 32
        gt = np.zeros((h, w), dtype=np.uint8)
        gt[10:20, 10:20] = 255

        # Inverted prediction
        pred = (1.0 - (gt.astype(np.float32) / 255.0))

        px_auroc = compute_pixel_auroc([gt], [pred])
        assert pytest.approx(px_auroc, 1e-4) == 0.0

    def test_zero_detections_no_crash(self):
        """
        Images with zero detected instances must return all-zero map and zero FAR without crashing.
        """
        h, w = 64, 64
        a_map = masks_to_anomaly_map([], [], (h, w))
        assert a_map.shape == (h, w)
        assert np.all(a_map == 0.0)

        far = compute_false_alarm_rate([], conf_threshold=0.25)
        assert far == 0.0

    def test_dual_domain_evaluator_group_aggregation(self):
        """
        Verify DualDomainEvaluator aggregates results by Texture (grid) and Object (screw) groups.
        """
        evaluator = DualDomainEvaluator(target_categories=["grid", "screw"])
        h, w = 32, 32

        # 1 Texture result (grid)
        m1 = np.zeros((h, w), dtype=np.uint8)
        m1[5:15, 5:15] = 255
        p1 = masks_to_anomaly_map([m1], [0.9], (h, w))
        r1 = evaluator.evaluate_category(
            category="grid",
            defect_gt_masks=[m1],
            defect_pred_maps=[p1],
            defect_max_confs=[0.9],
            good_max_confs=[0.1],
            mask_map50=0.85,
        )
        assert r1["group"] == "Texture"

        # 1 Object result (screw)
        m2 = np.zeros((h, w), dtype=np.uint8)
        m2[10:20, 10:20] = 255
        p2 = masks_to_anomaly_map([m2], [0.8], (h, w))
        r2 = evaluator.evaluate_category(
            category="screw",
            defect_gt_masks=[m2],
            defect_pred_maps=[p2],
            defect_max_confs=[0.8],
            good_max_confs=[0.05],
            mask_map50=0.75,
        )
        assert r2["group"] == "Object"

        summary = evaluator.aggregate_results([r1, r2])
        assert "texture_group_mean" in summary
        assert "object_group_mean" in summary
        assert "overall_mean" in summary
        assert summary["overall_mean"]["mask_mAP50"] == 0.80


class TestRobustnessEvaluator:
    def test_robustness_benchmark_execution(self):
        """
        Tests RobustnessEvaluator across corruptions and severities.
        """
        tmp_dir = tempfile.mkdtemp()
        try:
            evaluator = RobustnessEvaluator(
                corruptions=["gaussian_noise", "gaussian_blur"],
                severity_levels=[1, 2],
                output_dir=tmp_dir,
            )

            h, w = 32, 32
            img = np.full((h, w, 3), 120, dtype=np.uint8)
            gt_m = np.zeros((h, w), dtype=np.uint8)
            gt_m[8:16, 8:16] = 255

            def mock_predict(x):
                # Simple mock predictor
                a_map = np.zeros((h, w), dtype=np.float32)
                a_map[8:16, 8:16] = 0.8
                return a_map, 0.8

            df = evaluator.run_robustness_benchmark(
                images=[img],
                gt_masks=[gt_m],
                predict_fn=mock_predict,
                experiment_id="test_exp",
            )

            # 1 clean + (2 corruptions * 2 severities) = 5 rows
            assert len(df) == 5
            assert "pixel_auroc" in df.columns
            assert "mean_iou" in df.columns
            assert os.path.exists(os.path.join(tmp_dir, "test_exp_robustness_curves.csv"))
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)


class TestAblationMatrix:
    def test_collect_ablation_results(self, tmp_path):
        res_dir = tmp_path / "experiments"
        (res_dir / "exp00").mkdir(parents=True)

        summary_data = {
            "overall_mean": {"mask_mAP50": 0.82, "pixel_auroc": 0.95},
            "texture_group_mean": {"mask_mAP50": 0.88, "pixel_auroc": 0.97},
            "object_group_mean": {"mask_mAP50": 0.76, "pixel_auroc": 0.93},
        }
        import json
        with open(res_dir / "exp00" / "summary.json", "w") as f:
            json.dump(summary_data, f)

        df = collect_ablation_results(results_root=str(res_dir))
        assert len(df) == 1
        assert df.iloc[0]["Experiment"] == "exp00"
        assert df.iloc[0]["Mask_mAP50"] == 0.82
