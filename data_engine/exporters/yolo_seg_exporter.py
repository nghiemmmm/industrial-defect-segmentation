import os
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import cv2
import numpy as np

from data_engine.base import BaseExporter
from data_engine.sample import Sample

logger = logging.getLogger(__name__)


class YOLOSegExporter(BaseExporter):
    """
    Exports Sample instances to Ultralytics YOLO segmentation dataset format.

    Directory layout:
        output_dir/
            images/
                train/
                val/
            labels/
                train/
                val/
            masks_debug/  (optional, if save_debug_masks=True)
                train/
                val/
            dataset.yaml
            pipeline_meta.json
    """

    def __init__(
        self,
        output_dir: str,
        category_map: Optional[Dict[str, int]] = None,
        save_debug_masks: bool = False,
        image_format: str = "png",
        min_contour_points: int = 3,
        **kwargs,
    ):
        super().__init__(output_dir, **kwargs)
        self.category_map = category_map
        self.save_debug_masks = save_debug_masks
        self.image_format = image_format.lower()
        self.min_contour_points = min_contour_points

    def _ensure_category_map(self, samples: List[Sample]) -> Dict[str, int]:
        """Automatically builds sorted category -> ID map if not provided."""
        if self.category_map is not None:
            return self.category_map

        unique_categories = sorted(list(set(s.category for s in samples)))
        self.category_map = {cat: idx for idx, cat in enumerate(unique_categories)}
        return self.category_map

    def _mask_to_yolo_polygons(
        self,
        mask: np.ndarray,
        class_id: int,
        img_h: int,
        img_w: int,
    ) -> List[str]:
        """
        Converts binary mask to normalized YOLO polygon label strings.
        Format: "<class_id> x1 y1 x2 y2 x3 y3 ..."
        """
        if mask is None or not np.any(mask > 0):
            return []

        # Find external contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        lines = []

        for contour in contours:
            if len(contour) < self.min_contour_points:
                continue

            # Flatten and normalize
            points = contour.reshape(-1, 2)
            norm_points = []
            for pt in points:
                nx = max(0.0, min(1.0, pt[0] / img_w))
                ny = max(0.0, min(1.0, pt[1] / img_h))
                norm_points.append(f"{nx:.6f} {ny:.6f}")

            lines.append(f"{class_id} " + " ".join(norm_points))

        return lines

    def export(
        self,
        samples: List[Sample],
        split: str = "train",
        dataset_name: str = "industrial_defects",
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Exports samples into the YOLO segmentation folder structure.
        """
        category_map = self._ensure_category_map(samples)

        img_dir = os.path.join(self.output_dir, "images", split)
        lbl_dir = os.path.join(self.output_dir, "labels", split)
        os.makedirs(img_dir, exist_ok=True)
        os.makedirs(lbl_dir, exist_ok=True)

        dbg_dir = None
        if self.save_debug_masks:
            dbg_dir = os.path.join(self.output_dir, "masks_debug", split)
            os.makedirs(dbg_dir, exist_ok=True)

        stats = {
            "total_exported": 0,
            "anomalies": 0,
            "defect_free": 0,
            "total_contours": 0,
            "per_category": {cat: 0 for cat in category_map},
        }

        for idx, sample in enumerate(samples):
            # Formulate safe unique filename
            base_id = os.path.splitext(os.path.basename(sample.image_path))[0] if sample.image_path else f"{idx:05d}"
            filename_base = f"{sample.category}_{sample.defect_type}_{base_id}"
            
            img_filename = f"{filename_base}.{self.image_format}"
            lbl_filename = f"{filename_base}.txt"

            img_out_path = os.path.join(img_dir, img_filename)
            lbl_out_path = os.path.join(lbl_dir, lbl_filename)

            # 1. Save Image (convert back to BGR for OpenCV saving)
            bgr_image = cv2.cvtColor(sample.image, cv2.COLOR_RGB2BGR) if len(sample.image.shape) == 3 else sample.image
            cv2.imwrite(img_out_path, bgr_image)

            # 2. Save Label
            class_id = category_map[sample.category]
            h, w = sample.height, sample.width

            if sample.has_mask():
                polygon_lines = self._mask_to_yolo_polygons(sample.mask, class_id, h, w)
                with open(lbl_out_path, "w", encoding="utf-8") as f:
                    for line in polygon_lines:
                        f.write(line + "\n")

                stats["anomalies"] += 1
                stats["total_contours"] += len(polygon_lines)

                # Save debug mask if requested
                if dbg_dir and sample.mask is not None:
                    cv2.imwrite(os.path.join(dbg_dir, f"{filename_base}_mask.png"), sample.mask)
            else:
                # Defect-free / normal background sample -> empty file
                with open(lbl_out_path, "w", encoding="utf-8") as f:
                    pass
                stats["defect_free"] += 1

            stats["total_exported"] += 1
            stats["per_category"][sample.category] += 1

        # 3. Create or Update dataset.yaml
        yaml_path = os.path.join(self.output_dir, "dataset.yaml")
        yaml_content = (
            f"# Generated by DataEngine on {datetime.now().isoformat()}\n"
            f"path: .\n"
            f"train: images/train\n"
            f"val: images/val\n\n"
            f"names:\n"
        )
        for cat, cid in sorted(category_map.items(), key=lambda x: x[1]):
            yaml_content += f"  {cid}: {cat}\n"

        with open(yaml_path, "w", encoding="utf-8") as f:
            f.write(yaml_content)

        # 4. Save metadata record
        meta_path = os.path.join(self.output_dir, "pipeline_meta.json")
        existing_meta = {}
        if os.path.exists(meta_path):
            try:
                with open(meta_path, "r", encoding="utf-8") as f:
                    existing_meta = json.load(f)
            except Exception:
                existing_meta = {}

        existing_meta[split] = {
            "exported_at": datetime.now().isoformat(),
            "stats": stats,
        }
        existing_meta["dataset_name"] = dataset_name
        existing_meta["category_map"] = category_map

        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(existing_meta, f, indent=2)

        logger.info(
            f"Exported split '{split}' to {self.output_dir}: "
            f"{stats['total_exported']} images ({stats['anomalies']} anomalies, {stats['defect_free']} normal)."
        )
        return stats
