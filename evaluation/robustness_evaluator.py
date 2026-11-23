"""
MVTec-AD-C Robustness Evaluator.
Evaluates trained models across 4 optical/sensor corruption types
(Gaussian noise, Gaussian blur, Motion blur, Defocus blur) across 5 severity levels (1 to 5).
Outputs degradation curves to CSV and JSON for scientific analysis and plotting.
"""

from typing import Dict, Any, List, Optional
import os
import json
import pandas as pd
import numpy as np

from data_engine.corruptions.corruptions_engine import apply_corruption, SUPPORTED_CORRUPTIONS
from evaluation.dual_domain_metrics import compute_pixel_auroc, compute_image_auroc, compute_mask_iou


class RobustnessEvaluator:
    """
    Executes the MVTec-AD-C robustness protocol on a trained defect segmentation model.
    """

    def __init__(
        self,
        corruptions: Optional[List[str]] = None,
        severity_levels: Optional[List[int]] = None,
        output_dir: str = "results/robustness",
    ):
        self.corruptions = corruptions or list(SUPPORTED_CORRUPTIONS)
        self.severity_levels = severity_levels or [1, 2, 3, 4, 5]
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def evaluate_corrupted_batch(
        self,
        images: List[np.ndarray],
        gt_masks: List[np.ndarray],
        corruption_type: str,
        severity: int,
        predict_fn,  # callable(img) -> (anomaly_map, max_conf)
    ) -> Dict[str, Any]:
        """
        Applies corruption of specified type and severity to all images,
        runs predictions, and computes degradation metrics.
        """
        corrupted_images = [apply_corruption(img, corruption_type, severity) for img in images]

        pred_maps = []
        pred_confs = []
        gt_is_anomaly = []

        for c_img, gt_m in zip(corrupted_images, gt_masks):
            a_map, conf = predict_fn(c_img)
            pred_maps.append(a_map)
            pred_confs.append(conf)
            gt_is_anomaly.append(1 if np.any(gt_m > 0) else 0)

        # Compute metrics under corruption
        pixel_auroc = compute_pixel_auroc(gt_masks, pred_maps)
        image_auroc = compute_image_auroc(gt_is_anomaly, pred_confs)

        ious = []
        for p_m, g_m in zip(pred_maps, gt_masks):
            p_bin = (p_m >= 0.5).astype(np.uint8) * 255
            ious.append(compute_mask_iou(p_bin, g_m))
        mean_iou = float(np.mean(ious)) if ious else 0.0

        return {
            "corruption": corruption_type,
            "severity": severity,
            "pixel_auroc": round(pixel_auroc, 4),
            "image_auroc": round(image_auroc, 4),
            "mean_iou": round(mean_iou, 4),
        }

    def run_robustness_benchmark(
        self,
        images: List[np.ndarray],
        gt_masks: List[np.ndarray],
        predict_fn,
        experiment_id: str = "exp_baseline",
    ) -> pd.DataFrame:
        """
        Executes full matrix: 4 corruptions x 5 severity levels = 20 evaluation runs.
        """
        records = []

        # Baseline clean run (severity = 0)
        clean_maps = []
        clean_confs = []
        gt_is_anomaly = [1 if np.any(m > 0) else 0 for m in gt_masks]
        for img in images:
            a_map, conf = predict_fn(img)
            clean_maps.append(a_map)
            clean_confs.append(conf)

        clean_p_auroc = compute_pixel_auroc(gt_masks, clean_maps)
        clean_i_auroc = compute_image_auroc(gt_is_anomaly, clean_confs)
        clean_iou = float(np.mean([compute_mask_iou((m >= 0.5).astype(np.uint8) * 255, gm) for m, gm in zip(clean_maps, gt_masks)]))

        records.append({
            "experiment": experiment_id,
            "corruption": "clean",
            "severity": 0,
            "pixel_auroc": round(clean_p_auroc, 4),
            "image_auroc": round(clean_i_auroc, 4),
            "mean_iou": round(clean_iou, 4),
        })

        for c_type in self.corruptions:
            for sev in self.severity_levels:
                res = self.evaluate_corrupted_batch(
                    images=images,
                    gt_masks=gt_masks,
                    corruption_type=c_type,
                    severity=sev,
                    predict_fn=predict_fn,
                )
                res["experiment"] = experiment_id
                records.append(res)

        df = pd.DataFrame(records)
        csv_path = os.path.join(self.output_dir, f"{experiment_id}_robustness_curves.csv")
        json_path = os.path.join(self.output_dir, f"{experiment_id}_robustness_curves.json")
        df.to_csv(csv_path, index=False)
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2)

        return df
