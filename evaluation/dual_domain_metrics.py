"""
Dual-Domain Evaluation Metrics Calculator.
Implements:
1. Pixel-level anomaly probability map reconstruction from YOLO instance masks.
2. Pixel-level AUROC (roc_auc_score on flattened test masks).
3. Image-level AUROC (roc_auc_score on max image anomaly score vs binary ground-truth).
4. False Alarm Rate (FAR) on defect-free parts (test/good) at conf 0.25 and 0.50.
5. Segmentation metrics (Mask mAP50, Mask IoU).
6. Category group separation (Textures: grid, carpet, tile vs Objects: screw, pill, bottle).
"""

from typing import List, Dict, Any, Optional, Tuple
import numpy as np

try:
    from sklearn.metrics import roc_auc_score
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False


def _trapezoid_auc(fpr: np.ndarray, tpr: np.ndarray) -> float:
    """Computes AUC using standard trapezoidal rule."""
    order = np.argsort(fpr)
    fpr_s = fpr[order]
    tpr_s = tpr[order]
    return float(np.trapz(tpr_s, fpr_s))


def _pure_numpy_roc_auc_score(y_true: np.ndarray, y_score: np.ndarray) -> float:
    """
    Pure NumPy fallback for roc_auc_score when scikit-learn is unavailable.
    """
    y_true = np.asarray(y_true).ravel() > 0
    y_score = np.asarray(y_score).ravel()

    n_pos = np.sum(y_true)
    n_neg = len(y_true) - n_pos

    if n_pos == 0 or n_neg == 0:
        return 1.0 if np.all(y_score == y_score[0]) else 0.5

    # Sort descending
    desc_idx = np.argsort(-y_score)
    y_true_sorted = y_true[desc_idx]

    tps = np.cumsum(y_true_sorted)
    fps = np.cumsum(~y_true_sorted)

    tpr = np.r_[0, tps / n_pos, 1]
    fpr = np.r_[0, fps / n_neg, 1]

    return _trapezoid_auc(fpr, tpr)


def masks_to_anomaly_map(
    masks: List[np.ndarray],
    confidences: List[float],
    shape: Tuple[int, int],
) -> np.ndarray:
    """
    Converts YOLOv11-seg instance masks and confidence scores into a continuous
    Pixel-level anomaly probability map of size (H, W) in [0.0, 1.0].
    Takes pixel-wise maximum: max_i (conf_i * mask_i).
    If no instances detected, returns an all-zero map.
    """
    h, w = shape
    anomaly_map = np.zeros((h, w), dtype=np.float32)

    if not masks or not confidences:
        return anomaly_map

    for m, c in zip(masks, confidences):
        m_binary = (m > 0).astype(np.float32)
        if m_binary.shape[:2] != (h, w):
            m_binary = (m_binary > 0.5).astype(np.float32)
        anomaly_map = np.maximum(anomaly_map, m_binary * float(c))

    return np.clip(anomaly_map, 0.0, 1.0)


def compute_mask_iou(pred_mask: np.ndarray, gt_mask: np.ndarray) -> float:
    """
    Computes Intersection over Union (IoU) between binary prediction and ground-truth masks.
    """
    p = (pred_mask > 0)
    g = (gt_mask > 0)
    intersection = np.logical_and(p, g).sum()
    union = np.logical_or(p, g).sum()

    if union == 0:
        return 1.0 if intersection == 0 else 0.0
    return float(intersection / union)


def compute_pixel_auroc(
    gt_masks: List[np.ndarray],
    anomaly_maps: List[np.ndarray],
) -> float:
    """
    Computes Pixel-level AUROC across a collection of test images.
    Flattens all pixels and compares continuous anomaly maps against binary ground-truth.
    """
    if not gt_masks or not anomaly_maps:
        return 0.0

    gt_flat = (np.concatenate([np.asarray(m).ravel() for m in gt_masks]) > 0).astype(np.int32)
    pred_flat = np.concatenate([np.asarray(p).ravel() for p in anomaly_maps]).astype(np.float32)

    unique_gt = np.unique(gt_flat)
    if len(unique_gt) < 2:
        return 1.0 if np.all(pred_flat == pred_flat[0]) else 0.5

    if HAS_SKLEARN:
        return float(roc_auc_score(gt_flat, pred_flat))
    return _pure_numpy_roc_auc_score(gt_flat, pred_flat)


def compute_image_auroc(
    gt_is_anomaly: List[int],
    image_scores: List[float],
) -> float:
    """
    Computes Image-level AUROC for sample classification (defective vs normal).
    image_scores is typically max(confidence) or max(anomaly_map) per image.
    """
    gt_arr = np.asarray(gt_is_anomaly, dtype=np.int32)
    score_arr = np.asarray(image_scores, dtype=np.float32)

    unique_gt = np.unique(gt_arr)
    if len(unique_gt) < 2:
        return 1.0 if np.all(score_arr == score_arr[0]) else 0.5

    if HAS_SKLEARN:
        return float(roc_auc_score(gt_arr, score_arr))
    return _pure_numpy_roc_auc_score(gt_arr, score_arr)


def compute_false_alarm_rate(
    normal_predictions: List[float],
    conf_threshold: float = 0.25,
) -> float:
    """
    Calculates False Alarm Rate on defect-free parts (test/good).
    An image is a false alarm if model max confidence >= conf_threshold.
    """
    if not normal_predictions:
        return 0.0
    confs = np.asarray(normal_predictions, dtype=np.float32)
    fa_count = np.sum(confs >= conf_threshold)
    return float(fa_count / len(confs))


class DualDomainEvaluator:
    """
    Unified evaluator organizing evaluation per category and category groups
    (Textures: grid, carpet, tile vs Objects: screw, pill, bottle).
    """

    TEXTURE_CATEGORIES = {"grid", "carpet", "tile", "wood", "leather"}
    OBJECT_CATEGORIES = {"screw", "pill", "bottle", "capsule", "cable", "hazelnut", "metal_nut", "toothbrush", "transistor", "zipper"}

    def __init__(self, target_categories: Optional[List[str]] = None):
        self.target_categories = target_categories or [
            "grid", "carpet", "tile", "screw", "pill", "bottle"
        ]

    def evaluate_category(
        self,
        category: str,
        defect_gt_masks: List[np.ndarray],
        defect_pred_maps: List[np.ndarray],
        defect_max_confs: List[float],
        good_max_confs: List[float],
        box_map50: float = 0.0,
        mask_map50: float = 0.0,
        mask_map50_95: float = 0.0,
    ) -> Dict[str, Any]:
        """
        Evaluates metrics for a single category.
        """
        # 1. Pixel-level AUROC
        all_gt_masks = defect_gt_masks + [np.zeros_like(defect_gt_masks[0]) for _ in good_max_confs] if defect_gt_masks else []
        all_pred_maps = defect_pred_maps + [np.zeros_like(defect_gt_masks[0]) for _ in good_max_confs] if defect_gt_masks else []
        pixel_auroc = compute_pixel_auroc(all_gt_masks, all_pred_maps) if all_gt_masks else 0.0

        # 2. Image-level AUROC
        gt_sp = [1] * len(defect_max_confs) + [0] * len(good_max_confs)
        pr_sp = defect_max_confs + good_max_confs
        image_auroc = compute_image_auroc(gt_sp, pr_sp)

        # 3. False Alarm Rate on good parts
        far_025 = compute_false_alarm_rate(good_max_confs, conf_threshold=0.25)
        far_050 = compute_false_alarm_rate(good_max_confs, conf_threshold=0.50)

        # 4. Mean Mask IoU on defective parts
        ious = []
        for gt_m, pr_m in zip(defect_gt_masks, defect_pred_maps):
            pr_binary = (pr_m >= 0.5).astype(np.uint8) * 255
            ious.append(compute_mask_iou(pr_binary, gt_m))
        mean_mask_iou = float(np.mean(ious)) if ious else 0.0

        is_texture = category.lower() in self.TEXTURE_CATEGORIES
        group_type = "Texture" if is_texture else "Object"

        return {
            "category": category,
            "group": group_type,
            "num_defect_images": len(defect_max_confs),
            "num_good_images": len(good_max_confs),
            "mask_mAP50": round(float(mask_map50), 4),
            "mask_mAP50_95": round(float(mask_map50_95), 4),
            "box_mAP50": round(float(box_map50), 4),
            "mean_mask_iou": round(mean_mask_iou, 4),
            "pixel_auroc": round(pixel_auroc, 4),
            "image_auroc": round(image_auroc, 4),
            "false_alarm_rate_025": round(far_025, 4),
            "false_alarm_rate_050": round(far_050, 4),
        }

    def aggregate_results(self, category_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Aggregates category reports into Texture group, Object group, and Overall ALL summaries.
        """
        texture_res = [r for r in category_results if r["group"] == "Texture"]
        object_res = [r for r in category_results if r["group"] == "Object"]

        def _calc_mean(res_list: List[Dict[str, Any]]) -> Dict[str, float]:
            if not res_list:
                return {}
            keys = [
                "mask_mAP50", "mask_mAP50_95", "box_mAP50",
                "mean_mask_iou", "pixel_auroc", "image_auroc",
                "false_alarm_rate_025", "false_alarm_rate_050",
            ]
            return {k: round(float(np.mean([r[k] for r in res_list])), 4) for k in keys}

        return {
            "per_category": category_results,
            "texture_group_mean": _calc_mean(texture_res),
            "object_group_mean": _calc_mean(object_res),
            "overall_mean": _calc_mean(category_results),
        }
