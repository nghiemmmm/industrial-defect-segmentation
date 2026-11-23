"""
Parametric MVTec-AD-C Corruptions Engine.
Implements Gaussian Noise, Gaussian Blur, Motion Blur, and Defocus Blur across 5 severity levels.
"""

from typing import Tuple
import math
import random
import cv2
import numpy as np

SUPPORTED_CORRUPTIONS = ("gaussian_noise", "gaussian_blur", "motion_blur", "defocus_blur")


def apply_gaussian_noise(image: np.ndarray, severity: int = 1) -> np.ndarray:
    """
    Gaussian noise simulating sensor noise under low-light industrial inspection.
    Severity scales standard deviation sigma from 0.08 to 0.38 (normalized).
    """
    severity = max(1, min(5, severity))
    sigma_scales = [0.08, 0.12, 0.18, 0.26, 0.38]
    sigma = sigma_scales[severity - 1] * 255.0

    noise = np.random.normal(0, sigma, image.shape).astype(np.float32)
    corrupted = image.astype(np.float32) + noise
    return np.clip(corrupted, 0, 255).astype(np.uint8)


def apply_gaussian_blur(image: np.ndarray, severity: int = 1) -> np.ndarray:
    """
    Gaussian blur simulating optical lens defocus and soft focus.
    """
    severity = max(1, min(5, severity))
    sigmas = [1.0, 1.5, 2.0, 2.7, 3.5]
    sigma = sigmas[severity - 1]
    # Kernel size must be odd and at least 3
    ksize = int(math.ceil(2 * math.ceil(2 * sigma) + 1))
    if ksize % 2 == 0:
        ksize += 1

    return cv2.GaussianBlur(image, (ksize, ksize), sigmaX=sigma, sigmaY=sigma)


def apply_motion_blur(image: np.ndarray, severity: int = 1, angle: float = 45.0) -> np.ndarray:
    """
    Motion blur simulating industrial conveyor belt vibration or linear camera movement.
    """
    severity = max(1, min(5, severity))
    kernel_sizes = [10, 15, 20, 25, 30]
    size = kernel_sizes[severity - 1]

    # Generate 1D motion kernel and rotate by angle
    kernel = np.zeros((size, size), dtype=np.float32)
    kernel[int((size - 1) / 2), :] = np.ones(size, dtype=np.float32)

    M = cv2.getRotationMatrix2D((size / 2 - 0.5, size / 2 - 0.5), angle, 1.0)
    kernel = cv2.warpAffine(kernel, M, (size, size))
    kernel_sum = np.sum(kernel)
    if kernel_sum > 0:
        kernel = kernel / kernel_sum

    return cv2.filter2D(image, -1, kernel)


def apply_defocus_blur(image: np.ndarray, severity: int = 1) -> np.ndarray:
    """
    Defocus blur simulating out-of-depth-of-field (DoF) optical blur using a disk kernel.
    """
    severity = max(1, min(5, severity))
    radii = [3, 4, 6, 8, 10]
    radius = radii[severity - 1]

    ksize = 2 * radius + 1
    y, x = np.ogrid[-radius : radius + 1, -radius : radius + 1]
    mask = x ** 2 + y ** 2 <= radius ** 2
    kernel = np.zeros((ksize, ksize), dtype=np.float32)
    kernel[mask] = 1.0
    kernel_sum = np.sum(kernel)
    if kernel_sum > 0:
        kernel = kernel / kernel_sum

    return cv2.filter2D(image, -1, kernel)


def apply_corruption(image: np.ndarray, corruption_type: str, severity: int = 1) -> np.ndarray:
    """
    Unified entry point for applying parametric optical corruptions.
    """
    c_type = corruption_type.lower()
    if c_type == "gaussian_noise":
        return apply_gaussian_noise(image, severity)
    elif c_type == "gaussian_blur":
        return apply_gaussian_blur(image, severity)
    elif c_type == "motion_blur":
        return apply_motion_blur(image, severity)
    elif c_type == "defocus_blur":
        return apply_defocus_blur(image, severity)
    else:
        raise ValueError(
            f"Unsupported corruption: '{corruption_type}'. Choose from {SUPPORTED_CORRUPTIONS}"
        )
