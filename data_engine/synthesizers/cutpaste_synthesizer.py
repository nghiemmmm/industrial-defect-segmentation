"""
CutPaste and CutPaste-Scar Synthetic Anomaly Generator.
Based on Li et al., "CutPaste: Self-Supervised Learning for Anomaly Detection and Localization".
Pure NumPy and OpenCV implementation providing accurate pixel-level binary masks.
"""

from typing import Tuple, Optional
import math
import random
import cv2
import numpy as np

from data_engine.sample import Sample
from data_engine.synthesizers.base_synthesizer import BaseSynthesizer


class CutPasteSynthesizer(BaseSynthesizer):
    """
    CutPaste Synthetic Anomaly Generator.

    Supported Modes:
    - 'scar': Cuts a thin elongated strip (scar), rotates it at random angle,
              and pastes it with color jitter.
    - 'normal': Cuts a rectangular patch of specified area ratio and aspect ratio,
                and pastes it at a random destination with color jitter.
    - 'union': Randomly chooses between 'normal' and 'scar' with 50/50 probability.
    """

    def __init__(
        self,
        mode: str = "scar",
        scar_width: Tuple[int, int] = (2, 16),
        scar_height: Tuple[int, int] = (10, 35),
        scar_rotation: Tuple[float, float] = (-45.0, 45.0),
        area_ratio: Tuple[float, float] = (0.02, 0.15),
        aspect_ratio: float = 0.3,
        color_jitter: float = 0.15,
        anomaly_prob: float = 1.0,
        seed: Optional[int] = None,
        **kwargs,
    ):
        super().__init__(anomaly_prob=anomaly_prob, seed=seed, name="CutPaste", **kwargs)
        if mode not in ("scar", "normal", "union"):
            raise ValueError(f"Unknown mode: {mode}. Choose 'scar', 'normal', or 'union'.")
        self.mode = mode
        self.scar_width = scar_width
        self.scar_height = scar_height
        self.scar_rotation = scar_rotation
        self.area_ratio = area_ratio
        self.aspect_ratio = aspect_ratio
        self.color_jitter = color_jitter

    def _apply_color_jitter(self, patch: np.ndarray) -> np.ndarray:
        """Applies random brightness, contrast, and saturation jitter using OpenCV."""
        if self.color_jitter <= 0:
            return patch

        jittered = patch.astype(np.float32)

        # 1. Brightness jitter
        b_factor = 1.0 + random.uniform(-self.color_jitter, self.color_jitter)
        jittered = jittered * b_factor

        # 2. Contrast jitter
        c_factor = 1.0 + random.uniform(-self.color_jitter, self.color_jitter)
        mean_val = np.mean(jittered, axis=(0, 1), keepdims=True)
        jittered = (jittered - mean_val) * c_factor + mean_val

        jittered = np.clip(jittered, 0, 255).astype(np.uint8)

        # 3. Saturation jitter in HSV
        if jittered.shape[2] == 3:
            hsv = cv2.cvtColor(jittered, cv2.COLOR_RGB2HSV).astype(np.float32)
            s_factor = 1.0 + random.uniform(-self.color_jitter, self.color_jitter)
            hsv[:, :, 1] = np.clip(hsv[:, :, 1] * s_factor, 0, 255)
            jittered = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)

        return jittered

    def _cut_paste_normal(self, image: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        h, w = image.shape[:2]
        # Calculate random patch area
        ratio_area = random.uniform(self.area_ratio[0], self.area_ratio[1]) * w * h

        # Sample aspect ratio in log space
        log_min = math.log(self.aspect_ratio)
        log_max = math.log(1.0 / self.aspect_ratio)
        aspect = math.exp(random.uniform(log_min, log_max))

        cut_w = max(4, min(w - 2, int(round(math.sqrt(ratio_area * aspect)))))
        cut_h = max(4, min(h - 2, int(round(math.sqrt(ratio_area / aspect)))))

        from_y = random.randint(0, h - cut_h)
        from_x = random.randint(0, w - cut_w)
        patch = image[from_y : from_y + cut_h, from_x : from_x + cut_w].copy()

        # Apply color jitter
        patch = self._apply_color_jitter(patch)

        # Destination location
        to_y = random.randint(0, h - cut_h)
        to_x = random.randint(0, w - cut_w)

        # Paste onto image
        augmented_image = image.copy()
        augmented_image[to_y : to_y + cut_h, to_x : to_x + cut_w] = patch

        # Generate binary mask
        mask = np.zeros((h, w), dtype=np.uint8)
        mask[to_y : to_y + cut_h, to_x : to_x + cut_w] = 255

        return augmented_image, mask

    def _cut_paste_scar(self, image: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        h, w = image.shape[:2]
        cut_w = int(round(random.uniform(self.scar_width[0], self.scar_width[1])))
        cut_h = int(round(random.uniform(self.scar_height[0], self.scar_height[1])))
        cut_w = max(2, min(w - 2, cut_w))
        cut_h = max(2, min(h - 2, cut_h))

        from_y = random.randint(0, h - cut_h)
        from_x = random.randint(0, w - cut_w)
        patch = image[from_y : from_y + cut_h, from_x : from_x + cut_w].copy()

        # Apply color jitter
        patch = self._apply_color_jitter(patch)

        # Rotate patch using OpenCV affine rotation with expanded bounding box
        rot_deg = random.uniform(self.scar_rotation[0], self.scar_rotation[1])
        patch_mask = np.full((cut_h, cut_w), 255, dtype=np.uint8)

        # Calculate rotation matrix and new dimensions
        cx, cy = cut_w / 2.0, cut_h / 2.0
        M = cv2.getRotationMatrix2D((cx, cy), rot_deg, 1.0)
        cos_val = abs(M[0, 0])
        sin_val = abs(M[0, 1])
        new_w = int(cut_h * sin_val + cut_w * cos_val)
        new_h = int(cut_h * cos_val + cut_w * sin_val)
        M[0, 2] += (new_w / 2.0) - cx
        M[1, 2] += (new_h / 2.0) - cy

        rotated_patch = cv2.warpAffine(patch, M, (new_w, new_h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        rotated_mask = cv2.warpAffine(patch_mask, M, (new_w, new_h), flags=cv2.INTER_NEAREST, borderMode=cv2.BORDER_CONSTANT, borderValue=0)

        # Clean binary mask
        rotated_mask = np.where(rotated_mask > 127, 255, 0).astype(np.uint8)

        # Ensure rotated patch fits in destination
        if new_h >= h or new_w >= w:
            # Fallback to normal cutpaste if scar is too large for image
            return self._cut_paste_normal(image)

        to_y = random.randint(0, h - new_h)
        to_x = random.randint(0, w - new_w)

        augmented_image = image.copy()
        mask = np.zeros((h, w), dtype=np.uint8)

        # Blend rotated patch using its alpha mask
        alpha = (rotated_mask.astype(np.float32) / 255.0)[:, :, np.newaxis]
        target_roi = augmented_image[to_y : to_y + new_h, to_x : to_x + new_w].astype(np.float32)
        blended_roi = (1.0 - alpha) * target_roi + alpha * rotated_patch.astype(np.float32)

        augmented_image[to_y : to_y + new_h, to_x : to_x + new_w] = np.clip(blended_roi, 0, 255).astype(np.uint8)
        mask[to_y : to_y + new_h, to_x : to_x + new_w] = rotated_mask

        return augmented_image, mask

    def synthesize(self, sample: Sample) -> Sample:
        img = sample.image.copy()

        # Select mode
        active_mode = self.mode
        if active_mode == "union":
            active_mode = "scar" if random.random() < 0.5 else "normal"

        if active_mode == "scar":
            synth_img, synth_mask = self._cut_paste_scar(img)
            defect_name = "cutpaste_scar"
        else:
            synth_img, synth_mask = self._cut_paste_normal(img)
            defect_name = "cutpaste_normal"

        # Combine with any existing mask if present
        if sample.mask is not None and np.any(sample.mask > 0):
            combined_mask = np.maximum(sample.mask, synth_mask)
        else:
            combined_mask = synth_mask

        out_sample = sample.clone()
        out_sample.image = synth_img
        out_sample.mask = combined_mask
        out_sample.defect_type = defect_name
        out_sample.is_anomaly = bool(np.any(combined_mask > 0))
        return out_sample
