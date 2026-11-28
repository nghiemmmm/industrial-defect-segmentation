"""
MVTec-AD-C Robustness Evaluator.
Evaluates trained models across 4 optical/sensor corruption types
(Gaussian noise, Gaussian blur, Motion blur, Defocus blur) across 5 severity levels (1 to 5).
Outputs degradation curves to CSV and JSON for scientific analysis and plotting.
"""

from typing import Dict, Any, List, Optional
import gc
import os
import json
import cv2
import pandas as pd
import numpy as np

from data_engine.corruptions.corruptions_engine import apply_corruption, SUPPORTED_CORRUPTIONS
from evaluation.dual_domain_metrics import (
    compute_false_alarm_rate,
    compute_image_auroc,
    compute_mask_ap50,
    compute_mask_iou,
    compute_pixel_auroc,
)


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

    @staticmethod
    def _downsample_for_eval(arr: np.ndarray, max_size: int = 256, is_mask: bool = False) -> np.ndarray:
        if max_size and (arr.shape[0] > max_size or arr.shape[1] > max_size):
            interp = cv2.INTER_NEAREST if is_mask else cv2.INTER_LINEAR
            return cv2.resize(arr, (max_size, max_size), interpolation=interp)
        return arr

    def evaluate_corrupted_batch(
        self,
        images: List[np.ndarray],
        gt_masks: List[np.ndarray],
        corruption_type: str,
        severity: int,
        predict_fn,  # callable(img) -> (anomaly_map, max_conf)
        max_eval_size: int = 256,
    ) -> Dict[str, Any]:
        """
        Streams corruption one image at a time (avoiding 2GB+ RAM copies on Colab T4),
        runs predictions, and computes degradation metrics including Mask mAP@50 & FAR@0.25.
        """
        pred_maps = []
        eval_gt_masks = []
        pred_confs = []
        gt_is_anomaly = []
        ious = []

        for img, gt_m in zip(images, gt_masks):
            c_img = apply_corruption(img, corruption_type, severity)
            a_map, conf = predict_fn(c_img)
            del c_img

            gt_ds = self._downsample_for_eval(np.asarray(gt_m, dtype=np.uint8), max_eval_size, is_mask=True)
            am_ds = self._downsample_for_eval(np.asarray(a_map, dtype=np.float32), max_eval_size, is_mask=False)
            pred_maps.append(am_ds)
            eval_gt_masks.append(gt_ds)
            pred_confs.append(float(conf))
            gt_is_anomaly.append(1 if np.any(gt_ds > 0) else 0)
            ious.append(compute_mask_iou((am_ds >= 0.5).astype(np.uint8) * 255, gt_ds))

        # Compute metrics under corruption (including Mask mAP@50 & FAR@0.25 for Table V)
        pixel_auroc = compute_pixel_auroc(eval_gt_masks, pred_maps, max_eval_size=max_eval_size)
        image_auroc = compute_image_auroc(gt_is_anomaly, pred_confs)
        mask_map50 = compute_mask_ap50(eval_gt_masks, pred_maps, pred_confs)
        good_confs = [c for c, is_anom in zip(pred_confs, gt_is_anomaly) if is_anom == 0]
        far_025 = compute_false_alarm_rate(good_confs, conf_threshold=0.25)
        mean_iou = float(np.mean(ious)) if ious else 0.0

        del pred_maps, eval_gt_masks
        gc.collect()

        return {
            "corruption": corruption_type,
            "severity": severity,
            "mask_mAP50": round(mask_map50, 4),
            "far_025": round(far_025, 4),
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

        # Baseline clean run (severity = 0) with 256x256 downsampled eval buffers
        clean_maps = []
        clean_gt_masks = []
        clean_confs = []
        gt_is_anomaly = []
        clean_ious = []
        for img, gt_m in zip(images, gt_masks):
            a_map, conf = predict_fn(img)
            gt_ds = self._downsample_for_eval(np.asarray(gt_m, dtype=np.uint8), 256, is_mask=True)
            am_ds = self._downsample_for_eval(np.asarray(a_map, dtype=np.float32), 256, is_mask=False)
            clean_maps.append(am_ds)
            clean_gt_masks.append(gt_ds)
            clean_confs.append(float(conf))
            gt_is_anomaly.append(1 if np.any(gt_ds > 0) else 0)
            clean_ious.append(compute_mask_iou((am_ds >= 0.5).astype(np.uint8) * 255, gt_ds))

        clean_p_auroc = compute_pixel_auroc(clean_gt_masks, clean_maps, max_eval_size=256)
        clean_i_auroc = compute_image_auroc(gt_is_anomaly, clean_confs)
        clean_map50 = compute_mask_ap50(clean_gt_masks, clean_maps, clean_confs)
        clean_good_confs = [c for c, is_anom in zip(clean_confs, gt_is_anomaly) if is_anom == 0]
        clean_far_025 = compute_false_alarm_rate(clean_good_confs, conf_threshold=0.25)
        clean_iou = float(np.mean(clean_ious)) if clean_ious else 0.0
        del clean_maps, clean_gt_masks
        gc.collect()

        records.append({
            "experiment": experiment_id,
            "corruption": "clean",
            "severity": 0,
            "mask_mAP50": round(clean_map50, 4),
            "far_025": round(clean_far_025, 4),
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
