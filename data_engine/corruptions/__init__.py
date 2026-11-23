"""
Optical Degradation & Sensor Corruption Engine (Research Group C).
Conforms to MVTec-AD-C and ImageNet-C degradation benchmark protocols.
"""

from data_engine.corruptions.corruptions_engine import (
    apply_gaussian_noise,
    apply_gaussian_blur,
    apply_motion_blur,
    apply_defocus_blur,
    apply_corruption,
    SUPPORTED_CORRUPTIONS,
)

__all__ = [
    "apply_gaussian_noise",
    "apply_gaussian_blur",
    "apply_motion_blur",
    "apply_defocus_blur",
    "apply_corruption",
    "SUPPORTED_CORRUPTIONS",
]
