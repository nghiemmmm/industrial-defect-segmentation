"""
Natural Synthetic Anomalies (NSA) Synthesizer with Poisson Seamless Cloning.
Based on Schlüter et al., "Natural Synthetic Anomalies for Self-Supervised Anomaly Detection".
Features foreground object segmentation (for screw, pill, bottle) and seamless cloning.
"""

from typing import Tuple, Optional, List
import random
import cv2
import numpy as np

from data_engine.sample import Sample
from data_engine.synthesizers.base_synthesizer import BaseSynthesizer


class NSASynthesizer(BaseSynthesizer):
    """
    NSA Synthetic Anomaly Generator.

    Extracts natural texture/shape patches, applies color/scale shifts, and blends them
    into the destination using Poisson image editing (cv2.seamlessClone).
    Specifically constrains defect injection inside the object boundary for object categories.
    """

    OBJECT_CATEGORIES = {"screw", "pill", "bottle", "capsule", "cable", "hazelnut", "metal_nut", "toothbrush", "transistor", "zipper"}

    def __init__(
        self,
        width_ratio_range: Tuple[float, float] = (0.05, 0.25),
        height_ratio_range: Tuple[float, float] = (0.05, 0.25),
        resize_bounds: Tuple[float, float] = (0.7, 1.3),
        min_object_overlap: float = 0.5,
        clone_mode: int = cv2.NORMAL_CLONE,
        anomaly_prob: float = 1.0,
        seed: Optional[int] = None,
        **kwargs,
    ):
        super().__init__(anomaly_prob=anomaly_prob, seed=seed, name="NSA", **kwargs)
        self.width_ratio_range = width_ratio_range
        self.height_ratio_range = height_ratio_range
        self.resize_bounds = resize_bounds
        self.min_object_overlap = min_object_overlap
        self.clone_mode = clone_mode

    def _extract_foreground_mask(self, image: np.ndarray, category: str) -> np.ndarray:
        """
        Extracts foreground object mask. For texture categories (grid, carpet, tile),
        returns full mask. For object categories (screw, pill, bottle), detects object vs background.
        """
        h, w = image.shape[:2]
        if category.lower() not in self.OBJECT_CATEGORIES:
            # Textures cover the entire field of view
            return np.ones((h, w), dtype=np.uint8)

        # Estimate background color from the 5-pixel outer border
        border_pixels = np.concatenate([
            image[:5, :, :].reshape(-1, 3),
            image[-5:, :, :].reshape(-1, 3),
            image[:, :5, :].reshape(-1, 3),
            image[:, -5:, :].reshape(-1, 3),
        ], axis=0)
        bg_color = np.median(border_pixels, axis=0)

        # Distance from background color
        color_diff = np.linalg.norm(image.astype(np.float32) - bg_color, axis=-1)
        
        # Adaptive thresholding via Otsu on difference map
        norm_diff = cv2.normalize(color_diff, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        _, fg_thresh = cv2.threshold(norm_diff, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Clean noise via median blur and morphological closing
        fg_mask = cv2.medianBlur(fg_thresh, 7)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)

        # If foreground detection yielded almost nothing, fallback to full image
        if np.sum(fg_mask > 0) < (0.01 * h * w):
            return np.ones((h, w), dtype=np.uint8)

        return np.where(fg_mask > 0, 1, 0).astype(np.uint8)

    def _sample_patch(
        self,
        image: np.ndarray,
        fg_mask: np.ndarray,
    ) -> Optional[Tuple[np.ndarray, np.ndarray, Tuple[int, int, int, int]]]:
        """
        Samples a valid patch from within the image/object.
        Returns: (patch, patch_mask, (y1, y2, x1, x2))
        """
        h, w = image.shape[:2]
        min_w = max(8, int(self.width_ratio_range[0] * w))
        max_w = min(w - 10, int(self.width_ratio_range[1] * w))
        min_h = max(8, int(self.height_ratio_range[0] * h))
        max_h = min(h - 10, int(self.height_ratio_range[1] * h))

        if min_w >= max_w or min_h >= max_h:
            return None

        # Sample patch dimensions
        pw = random.randint(min_w, max_w)
        ph = random.randint(min_h, max_h)

        # Sample source coordinates with preference for foreground
        attempts = 0
        while attempts < 30:
            attempts += 1
            src_y = random.randint(0, h - ph)
            src_x = random.randint(0, w - pw)

            # Check overlap with foreground
            fg_overlap = np.mean(fg_mask[src_y : src_y + ph, src_x : src_x + pw])
            if fg_overlap >= self.min_object_overlap:
                patch = image[src_y : src_y + ph, src_x : src_x + pw].copy()
                
                # Apply random resizing
                scale = random.uniform(self.resize_bounds[0], self.resize_bounds[1])
                new_pw = max(8, min(w - 10, int(round(pw * scale))))
                new_ph = max(8, min(h - 10, int(round(ph * scale))))
                patch = cv2.resize(patch, (new_pw, new_ph), interpolation=cv2.INTER_LINEAR)

                # Generate patch mask (ellipse or rounded rect)
                pmask = np.zeros((new_ph, new_pw), dtype=np.uint8)
                cv2.ellipse(
                    pmask,
                    (new_pw // 2, new_ph // 2),
                    (new_pw // 2 - 1, new_ph // 2 - 1),
                    0, 0, 360, 255, -1
                )
                # Zero 1-pixel border to prevent cv2.seamlessClone boundary artifacts
                pmask[0, :] = 0
                pmask[-1, :] = 0
                pmask[:, 0] = 0
                pmask[:, -1] = 0

                if np.sum(pmask > 0) >= 50:
                    return patch, pmask, (src_y, src_y + ph, src_x, src_x + pw)

        return None

    def synthesize(self, sample: Sample) -> Sample:
        img = sample.image
        h, w = img.shape[:2]
        fg_mask = self._extract_foreground_mask(img, sample.category)

        sampled = self._sample_patch(img, fg_mask)
        if sampled is None:
            # If sampling failed, fallback to CutPaste normal
            cloned = sample.clone()
            return cloned

        patch, patch_mask, _ = sampled
        ph, pw = patch.shape[:2]

        # Find valid center inside foreground object
        fg_indices = np.argwhere(fg_mask > 0)
        valid_centers = []
        for y, x in fg_indices:
            if (ph // 2 + 1) < y < (h - ph // 2 - 1) and (pw // 2 + 1) < x < (w - pw // 2 - 1):
                valid_centers.append((x, y))  # (center_x, center_y) for OpenCV

        if not valid_centers:
            # Fallback if object is too small
            center_x = random.randint(pw // 2 + 1, w - pw // 2 - 1)
            center_y = random.randint(ph // 2 + 1, h - ph // 2 - 1)
        else:
            center_x, center_y = random.choice(valid_centers)

        # Calculate bounding box in target image
        y1 = center_y - ph // 2
        y2 = y1 + ph
        x1 = center_x - pw // 2
        x2 = x1 + pw

        # Color shift to create contrast difference
        shift_val = random.uniform(20.0, 60.0) * random.choice([-1.0, 1.0])
        patch_shifted = np.clip(patch.astype(np.float32) + shift_val, 0, 255).astype(np.uint8)

        # Execute Poisson Seamless Cloning
        augmented_image = img.copy()
        mask = np.zeros((h, w), dtype=np.uint8)

        try:
            augmented_image = cv2.seamlessClone(
                patch_shifted,
                img,
                patch_mask,
                (center_x, center_y),
                self.clone_mode
            )
            # Mark mask region intersecting foreground
            target_mask_roi = (patch_mask > 0).astype(np.uint8) * 255
            mask[y1:y2, x1:x2] = np.maximum(mask[y1:y2, x1:x2], target_mask_roi)
            if sample.category.lower() in self.OBJECT_CATEGORIES:
                mask = np.where(fg_mask > 0, mask, 0).astype(np.uint8)
        except cv2.error:
            # Fallback linear alpha blending if seamlessClone rejects gradient
            alpha = (patch_mask.astype(np.float32) / 255.0)[:, :, np.newaxis]
            roi = augmented_image[y1:y2, x1:x2].astype(np.float32)
            augmented_image[y1:y2, x1:x2] = np.clip(
                (1.0 - alpha) * roi + alpha * patch_shifted.astype(np.float32), 0, 255
            ).astype(np.uint8)
            mask[y1:y2, x1:x2] = patch_mask

        # Combine with existing mask
        if sample.mask is not None and np.any(sample.mask > 0):
            combined_mask = np.maximum(sample.mask, mask)
        else:
            combined_mask = mask

        out_sample = sample.clone()
        out_sample.image = augmented_image
        out_sample.mask = combined_mask
        out_sample.defect_type = "nsa_poisson"
        out_sample.is_anomaly = bool(np.any(combined_mask > 0))
        return out_sample
