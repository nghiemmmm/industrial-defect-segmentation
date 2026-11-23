"""
DRAEM Synthetic Anomaly Generator (Perlin Noise & Texture Blending).
Based on Zavrtanik et al., "DRAEM - A discriminatively trained reconstruction
anomaly embedding model for surface anomaly detection".
Faithful implementation of rand_perlin_2d_np and beta-blending with dual-mode
texture support (self-texture synthesis or DTD directory).
"""

import os
import glob
import math
import random
from typing import Tuple, Optional
import cv2
import numpy as np

from data_engine.sample import Sample
from data_engine.synthesizers.base_synthesizer import BaseSynthesizer


def lerp_np(x: np.ndarray, y: np.ndarray, w: np.ndarray) -> np.ndarray:
    return (y - x) * w + x


def rand_perlin_2d_np(
    shape: Tuple[int, int],
    res: Tuple[int, int],
    fade=lambda t: 6 * t ** 5 - 15 * t ** 4 + 10 * t ** 3,
) -> np.ndarray:
    """
    Exact NumPy implementation of 2D Perlin noise from VitjanZ/DRAEM,
    with canonical power-of-2 grid generation and bilinear interpolation
    to support arbitrary image shapes (e.g. 900x900 bottle, 840x840 tile).
    """
    res = (max(1, res[0]), max(1, res[1]))
    base_shape = (512, 512)
    delta = (res[0] / base_shape[0], res[1] / base_shape[1])
    d = (max(1, base_shape[0] // res[0]), max(1, base_shape[1] // res[1]))
    grid = np.mgrid[0:res[0]:delta[0], 0:res[1]:delta[1]].transpose(1, 2, 0) % 1

    angles = 2 * math.pi * np.random.rand(res[0] + 1, res[1] + 1)
    gradients = np.stack((np.cos(angles), np.sin(angles)), axis=-1)

    tile_grads = lambda s1, s2: np.repeat(
        np.repeat(gradients[s1[0]:s1[1], s2[0]:s2[1]], d[0], axis=0), d[1], axis=1
    )
    dot = lambda grad, shift: (
        np.stack(
            (grid[:base_shape[0], :base_shape[1], 0] + shift[0], grid[:base_shape[0], :base_shape[1], 1] + shift[1]),
            axis=-1,
        )
        * grad[:base_shape[0], :base_shape[1]]
    ).sum(axis=-1)

    n00 = dot(tile_grads([0, -1], [0, -1]), [0, 0])
    n10 = dot(tile_grads([1, None], [0, -1]), [-1, 0])
    n01 = dot(tile_grads([0, -1], [1, None]), [0, -1])
    n11 = dot(tile_grads([1, None], [1, None]), [-1, -1])
    t = fade(grid[:base_shape[0], :base_shape[1]])
    perlin = math.sqrt(2) * lerp_np(lerp_np(n00, n10, t[..., 0]), lerp_np(n01, n11, t[..., 0]), t[..., 1])

    if perlin.shape != shape:
        perlin = cv2.resize(perlin, (shape[1], shape[0]), interpolation=cv2.INTER_LINEAR)
    return perlin


class DRAEMSynthesizer(BaseSynthesizer):
    """
    DRAEM Anomaly Synthesizer.

    Generates realistic surface and structural anomalies by thresholding Perlin noise
    and blending with an anomaly texture (either self-texture augmentation or external DTD).
    """

    def __init__(
        self,
        dtd_dir: Optional[str] = None,
        perlin_scale_max: int = 6,
        perlin_scale_min: int = 0,
        perlin_threshold: float = 0.5,
        beta_range: Tuple[float, float] = (0.2, 0.8),
        anomaly_prob: float = 1.0,
        seed: Optional[int] = None,
        **kwargs,
    ):
        super().__init__(anomaly_prob=anomaly_prob, seed=seed, name="DRAEM", **kwargs)
        self.dtd_dir = dtd_dir
        self.perlin_scale_max = perlin_scale_max
        self.perlin_scale_min = perlin_scale_min
        self.perlin_threshold = perlin_threshold
        self.beta_range = beta_range

        self.dtd_images = []
        if dtd_dir and os.path.exists(dtd_dir):
            self.dtd_images = sorted(glob.glob(os.path.join(dtd_dir, "**", "*.jpg"), recursive=True))

    def _generate_self_anomaly_texture(self, image: np.ndarray) -> np.ndarray:
        """
        Creates an aggressive, realistic anomaly texture without external DTD.
        Applies non-linear color inversion, posterization, gamma shift, and edge enhancement.
        """
        h, w = image.shape[:2]
        tex = image.copy().astype(np.float32)

        aug_type = random.randint(0, 4)
        if aug_type == 0:
            # Solarize / partial invert
            threshold = random.uniform(64, 192)
            tex = np.where(tex > threshold, 255.0 - tex, tex)
        elif aug_type == 1:
            # High gamma contrast shift
            gamma = random.uniform(0.3, 3.0)
            tex = 255.0 * ((tex / 255.0) ** gamma)
        elif aug_type == 2:
            # Color channel shuffle + saturation boost
            hsv = cv2.cvtColor(np.clip(tex, 0, 255).astype(np.uint8), cv2.COLOR_RGB2HSV).astype(np.float32)
            hsv[:, :, 0] = (hsv[:, :, 0] + random.uniform(30, 150)) % 180
            hsv[:, :, 1] = np.clip(hsv[:, :, 1] * random.uniform(1.5, 2.5), 0, 255)
            tex = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB).astype(np.float32)
        elif aug_type == 3:
            # Posterization (quantization)
            step = random.choice([32, 64, 128])
            tex = np.floor(tex / step) * step
        else:
            # Frequency / Laplacian edge accentuation
            gray = cv2.cvtColor(np.clip(tex, 0, 255).astype(np.uint8), cv2.COLOR_RGB2GRAY)
            lap = cv2.Laplacian(gray, cv2.CV_32F)
            for c in range(3):
                tex[:, :, c] = np.clip(tex[:, :, c] + lap * random.uniform(1.0, 3.0), 0, 255)

        # Random affine rotation on anomaly texture
        center = (w // 2, h // 2)
        angle = random.uniform(-180, 180)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        tex = cv2.warpAffine(tex, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        return np.clip(tex, 0, 255).astype(np.uint8)

    def _sample_anomaly_texture(self, target_shape: Tuple[int, int], source_image: np.ndarray) -> np.ndarray:
        h, w = target_shape
        if self.dtd_images:
            sampled_path = random.choice(self.dtd_images)
            tex = cv2.imread(sampled_path, cv2.IMREAD_COLOR)
            if tex is not None:
                tex = cv2.cvtColor(tex, cv2.COLOR_BGR2RGB)
                return cv2.resize(tex, (w, h), interpolation=cv2.INTER_LINEAR)

        # Fallback to self-texture synthesis
        return self._generate_self_anomaly_texture(source_image)

    def synthesize(self, sample: Sample) -> Sample:
        img = sample.image
        h, w = img.shape[:2]

        # 1. Sample Perlin scale exponents
        sx = 2 ** random.randint(self.perlin_scale_min, self.perlin_scale_max)
        sy = 2 ** random.randint(self.perlin_scale_min, self.perlin_scale_max)

        # 2. Generate 2D Perlin noise
        perlin_map = rand_perlin_2d_np((h, w), (sx, sy))

        # 3. Rotate Perlin noise to avoid strictly axis-aligned artifacts
        rot_angle = random.uniform(-90.0, 90.0)
        M_rot = cv2.getRotationMatrix2D((w // 2, h // 2), rot_angle, 1.0)
        perlin_map = cv2.warpAffine(perlin_map, M_rot, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

        # 4. Binary thresholding to obtain defect mask
        binary_mask = np.where(perlin_map > self.perlin_threshold, 255, 0).astype(np.uint8)

        # If mask is empty due to high threshold, retry with lower threshold or generate ellipse
        if not np.any(binary_mask > 0):
            binary_mask = np.where(perlin_map > (self.perlin_threshold * 0.7), 255, 0).astype(np.uint8)

        # 5. Fetch anomaly texture
        anomaly_texture = self._sample_anomaly_texture((h, w), img)

        # 6. Beta blending: I_synth = (1 - M) * I + M * ((1 - beta) * I_anom + beta * I)
        beta = random.uniform(self.beta_range[0], self.beta_range[1])
        mask_f = (binary_mask.astype(np.float32) / 255.0)[:, :, np.newaxis]
        img_f = img.astype(np.float32)
        tex_f = anomaly_texture.astype(np.float32)

        blended_defect = (1.0 - beta) * tex_f + beta * img_f
        synth_img = (1.0 - mask_f) * img_f + mask_f * blended_defect
        synth_img = np.clip(synth_img, 0, 255).astype(np.uint8)

        # Combine with existing mask if present
        if sample.mask is not None and np.any(sample.mask > 0):
            combined_mask = np.maximum(sample.mask, binary_mask)
        else:
            combined_mask = binary_mask

        out_sample = sample.clone()
        out_sample.image = synth_img
        out_sample.mask = combined_mask
        out_sample.defect_type = "draem_perlin"
        out_sample.is_anomaly = bool(np.any(combined_mask > 0))
        return out_sample
