import os
import random
import logging
from typing import List, Optional, Tuple, Dict
import cv2
import numpy as np

from data_engine.base import BaseDatasetLoader
from data_engine.sample import Sample

logger = logging.getLogger(__name__)


class MVTecLoader(BaseDatasetLoader):
    """
    Standard Loader for the MVTec Anomaly Detection (MVTec AD) dataset.

    Supports:
    - Automatic category discovery (bottle, cable, screw, tile, etc.)
    - Clean paired loading of defect images with their corresponding ground-truth masks
    - Loading normal (defect-free) parts from train/good and test/good to control false alarm rates
    - Controlled negative sample ratio (good_ratio)
    - Deterministic, seeded train/val splitting per defect type
    - Data integrity checks (shape matching, missing masks)
    """

    def __init__(
        self,
        root_dir: str,
        split_ratio: float = 0.8,
        include_good_train: bool = True,
        good_ratio: Optional[float] = None,
        seed: int = 42,
        **kwargs,
    ):
        super().__init__(root_dir, **kwargs)
        self.split_ratio = split_ratio
        self.include_good_train = include_good_train
        self.good_ratio = good_ratio
        self.seed = seed

    def get_categories(self) -> List[str]:
        """Finds all valid category directories containing 'test' or 'ground_truth'."""
        if not os.path.exists(self.root_dir):
            raise FileNotFoundError(f"MVTec root directory not found: {self.root_dir}")

        categories = sorted([
            d for d in os.listdir(self.root_dir)
            if os.path.isdir(os.path.join(self.root_dir, d))
            and os.path.exists(os.path.join(self.root_dir, d, "test"))
        ])
        return categories

    def _read_image(self, path: str) -> np.ndarray:
        """Reads image from disk in RGB format."""
        img = cv2.imread(path, cv2.IMREAD_COLOR)
        if img is None:
            raise IOError(f"Failed to read image from {path}")
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    def _read_mask(self, mask_path: str, expected_shape: Tuple[int, int]) -> np.ndarray:
        """Reads binary mask in grayscale. If missing or invalid, raises or returns zero mask."""
        if not os.path.exists(mask_path):
            logger.warning(f"Mask file not found at {mask_path}. Defaulting to zero mask.")
            return np.zeros(expected_shape, dtype=np.uint8)

        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
        if mask is None:
            raise IOError(f"Failed to read mask from {mask_path}")

        # Binarize mask (ensure 0 or 255)
        _, binary_mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
        
        # Verify shape
        if binary_mask.shape[:2] != expected_shape:
            logger.warning(
                f"Mask shape {binary_mask.shape[:2]} does not match image shape {expected_shape}. Resizing mask."
            )
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
        """
        Loads samples for specified categories and split.

        Args:
            categories: List of category names or None to load all available.
            split: 'train' or 'val'.
            load_images: If False, images/masks are not loaded into memory (dummy empty arrays),
                         only metadata and paths are populated (useful for fast indexing).
        """
        all_categories = self.get_categories()
        target_categories = [c for c in (categories or all_categories) if c in all_categories]

        if not target_categories:
            logger.warning(f"No matching categories found in {self.root_dir}")
            return []

        rng = random.Random(self.seed)
        samples: List[Sample] = []

        for cat in target_categories:
            cat_dir = os.path.join(self.root_dir, cat)
            test_dir = os.path.join(cat_dir, "test")
            gt_dir = os.path.join(cat_dir, "ground_truth")
            train_dir = os.path.join(cat_dir, "train")

            # 1. Collect anomaly samples from test/<defect_type>/
            defect_types = sorted([d for d in os.listdir(test_dir) if d != "good" and os.path.isdir(os.path.join(test_dir, d))])
            
            cat_train_defects: List[Dict] = []
            cat_val_defects: List[Dict] = []

            for defect in defect_types:
                img_folder = os.path.join(test_dir, defect)
                defect_gt_folder = os.path.join(gt_dir, defect)
                img_files = sorted([f for f in os.listdir(img_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
                
                # Shuffle deterministically per defect type
                rng.shuffle(img_files)
                split_idx = int(len(img_files) * self.split_ratio)
                train_files = img_files[:split_idx]
                val_files = img_files[split_idx:]

                for f in train_files:
                    cat_train_defects.append({
                        "category": cat,
                        "defect": defect,
                        "img_path": os.path.join(img_folder, f),
                        "mask_path": os.path.join(defect_gt_folder, f.rsplit(".", 1)[0] + "_mask.png"),
                        "is_anomaly": True
                    })
                for f in val_files:
                    cat_val_defects.append({
                        "category": cat,
                        "defect": defect,
                        "img_path": os.path.join(img_folder, f),
                        "mask_path": os.path.join(defect_gt_folder, f.rsplit(".", 1)[0] + "_mask.png"),
                        "is_anomaly": True
                    })

            # 2. Collect normal (good) samples
            good_train_imgs = []
            if self.include_good_train and os.path.exists(os.path.join(train_dir, "good")):
                good_folder = os.path.join(train_dir, "good")
                good_train_imgs = sorted([
                    os.path.join(good_folder, f)
                    for f in os.listdir(good_folder)
                    if f.lower().endswith(('.png', '.jpg', '.jpeg'))
                ])
                rng.shuffle(good_train_imgs)

            # Apply good_ratio if specified (e.g. 0.10 of defect count)
            if self.good_ratio is not None and cat_train_defects:
                max_good = int(len(cat_train_defects) * self.good_ratio)
                good_train_imgs = good_train_imgs[:max_good]

            # Choose entries based on requested split
            selected_entries = []
            if split == "train":
                selected_entries.extend(cat_train_defects)
                for g_path in good_train_imgs:
                    selected_entries.append({
                        "category": cat,
                        "defect": "good",
                        "img_path": g_path,
                        "mask_path": None,
                        "is_anomaly": False
                    })
            elif split == "val":
                selected_entries.extend(cat_val_defects)
            elif split == "all":
                selected_entries.extend(cat_train_defects)
                selected_entries.extend(cat_val_defects)
                for g_path in good_train_imgs:
                    selected_entries.append({
                        "category": cat,
                        "defect": "good",
                        "img_path": g_path,
                        "mask_path": None,
                        "is_anomaly": False
                    })

            # 3. Instantiate Sample objects
            for entry in selected_entries:
                img_path = entry["img_path"]
                if load_images:
                    img = self._read_image(img_path)
                    h, w = img.shape[:2]
                    if entry["is_anomaly"] and entry["mask_path"]:
                        mask = self._read_mask(entry["mask_path"], (h, w))
                    else:
                        mask = np.zeros((h, w), dtype=np.uint8)
                else:
                    img = np.zeros((1, 1, 3), dtype=np.uint8)
                    mask = np.zeros((1, 1), dtype=np.uint8)

                sample = Sample(
                    image=img,
                    mask=mask,
                    category=entry["category"],
                    defect_type=entry["defect"],
                    is_anomaly=entry["is_anomaly"],
                    image_path=img_path,
                    metadata={"split": split, "source": "MVTec AD"},
                )
                samples.append(sample)

        logger.info(f"Loaded {len(samples)} samples for split='{split}' across {len(target_categories)} categories.")
        return samples
