import os
import random
import logging
from typing import List, Optional, Tuple, Dict
import cv2
import numpy as np

from data_engine.base import BaseDatasetLoader
from data_engine.sample import Sample

logger = logging.getLogger(__name__)


class VisALoader(BaseDatasetLoader):
    """
    Standard Loader for the Visual Anomaly (VisA) dataset.

    Supports:
    - Discovery of VisA categories (pcb1-4, capsules, candle, cashew, etc.)
    - Paired loading of anomaly images with their ground-truth masks
    - Loading normal (background) images with controllable balancing (good_ratio)
    - Deterministic train/val split
    """

    def __init__(
        self,
        root_dir: str,
        split_ratio: float = 0.8,
        good_ratio: Optional[float] = 0.10,
        seed: int = 42,
        **kwargs,
    ):
        super().__init__(root_dir, **kwargs)
        self.split_ratio = split_ratio
        self.good_ratio = good_ratio
        self.seed = seed

    def get_categories(self) -> List[str]:
        if not os.path.exists(self.root_dir):
            raise FileNotFoundError(f"VisA root directory not found: {self.root_dir}")

        categories = []
        for d in sorted(os.listdir(self.root_dir)):
            cat_path = os.path.join(self.root_dir, d)
            if not os.path.isdir(cat_path):
                continue
            # Check if this directory looks like a VisA category
            subdirs = os.listdir(cat_path)
            if "anomaly" in subdirs or "normal" in subdirs or "Data" in subdirs:
                categories.append(d)
        return categories

    def _read_image(self, path: str) -> np.ndarray:
        img = cv2.imread(path, cv2.IMREAD_COLOR)
        if img is None:
            raise IOError(f"Failed to read image from {path}")
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    def _read_mask(self, mask_path: str, expected_shape: Tuple[int, int]) -> np.ndarray:
        if not os.path.exists(mask_path):
            logger.warning(f"Mask file not found at {mask_path}. Defaulting to zero mask.")
            return np.zeros(expected_shape, dtype=np.uint8)

        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
        if mask is None:
            raise IOError(f"Failed to read mask from {mask_path}")

        _, binary_mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
        if binary_mask.shape[:2] != expected_shape:
            binary_mask = cv2.resize(
                binary_mask, (expected_shape[1], expected_shape[0]), interpolation=cv2.INTER_NEAREST
            )
        return binary_mask

    def load(
        self,
        categories: Optional[List[str]] = None,
        split: str = "train",
        load_images: bool = True,
    ) -> List[Sample]:
        all_categories = self.get_categories()
        target_categories = [c for c in (categories or all_categories) if c in all_categories]

        if not target_categories:
            logger.warning(f"No matching VisA categories found in {self.root_dir}")
            return []

        rng = random.Random(self.seed)
        samples: List[Sample] = []

        for cat in target_categories:
            cat_dir = os.path.join(self.root_dir, cat)
            if os.path.exists(os.path.join(cat_dir, "Data")):
                cat_dir = os.path.join(cat_dir, "Data")

            anomaly_dir = os.path.join(cat_dir, "anomaly")
            normal_dir = os.path.join(cat_dir, "normal")
            gt_dir = os.path.join(cat_dir, "ground_truth")

            # Collect anomaly images
            anomaly_files = []
            if os.path.exists(anomaly_dir):
                anomaly_files = sorted([
                    f for f in os.listdir(anomaly_dir)
                    if f.lower().endswith(('.png', '.jpg', '.jpeg'))
                ])
                rng.shuffle(anomaly_files)

            split_idx = int(len(anomaly_files) * self.split_ratio)
            anomaly_subset = anomaly_files[:split_idx] if split == "train" else anomaly_files[split_idx:]
            if split == "all":
                anomaly_subset = anomaly_files

            for f in anomaly_subset:
                img_path = os.path.join(anomaly_dir, f)
                mask_candidate = os.path.join(gt_dir, f.rsplit(".", 1)[0] + ".png")
                if not os.path.exists(mask_candidate):
                    mask_candidate = os.path.join(gt_dir, f.rsplit(".", 1)[0] + "_mask.png")

                if load_images:
                    img = self._read_image(img_path)
                    h, w = img.shape[:2]
                    mask = self._read_mask(mask_candidate, (h, w))
                else:
                    img = np.zeros((1, 1, 3), dtype=np.uint8)
                    mask = np.zeros((1, 1), dtype=np.uint8)

                samples.append(
                    Sample(
                        image=img,
                        mask=mask,
                        category=cat,
                        defect_type="anomaly",
                        is_anomaly=True,
                        image_path=img_path,
                        metadata={"split": split, "source": "VisA"},
                    )
                )

            # Collect normal images
            if os.path.exists(normal_dir) and split in ("train", "all"):
                normal_files = sorted([
                    f for f in os.listdir(normal_dir)
                    if f.lower().endswith(('.png', '.jpg', '.jpeg'))
                ])
                rng.shuffle(normal_files)

                if self.good_ratio is not None and len(anomaly_subset) > 0:
                    max_normal = int(len(anomaly_subset) * self.good_ratio)
                    normal_files = normal_files[:max_normal]

                for f in normal_files:
                    img_path = os.path.join(normal_dir, f)
                    if load_images:
                        img = self._read_image(img_path)
                        h, w = img.shape[:2]
                        mask = np.zeros((h, w), dtype=np.uint8)
                    else:
                        img = np.zeros((1, 1, 3), dtype=np.uint8)
                        mask = np.zeros((1, 1), dtype=np.uint8)

                    samples.append(
                        Sample(
                            image=img,
                            mask=mask,
                            category=cat,
                            defect_type="normal",
                            is_anomaly=False,
                            image_path=img_path,
                            metadata={"split": split, "source": "VisA"},
                        )
                    )

        logger.info(f"Loaded {len(samples)} VisA samples for split='{split}'.")
        return samples
