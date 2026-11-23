"""
Dual-Domain Evaluation Framework.
Combines YOLOv11 Segmentation Metrics (Mask mAP, IoU)
with Industrial Anomaly Detection Benchmark Metrics (Pixel-AUROC, Image-AUROC, FAR).
"""

from evaluation.dual_domain_metrics import (
    masks_to_anomaly_map,
    compute_mask_iou,
    compute_pixel_auroc,
    compute_image_auroc,
    compute_false_alarm_rate,
    DualDomainEvaluator,
)

__all__ = [
    "masks_to_anomaly_map",
    "compute_mask_iou",
    "compute_pixel_auroc",
    "compute_image_auroc",
    "compute_false_alarm_rate",
    "DualDomainEvaluator",
]
