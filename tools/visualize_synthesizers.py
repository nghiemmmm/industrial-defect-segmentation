#!/usr/bin/env python3
"""
Visual verification script: Demonstrates CutPaste, DRAEM, and NSA anomaly synthesis.
Saves a side-by-side comparison image to results/figures/synthetic_preview.png.
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import cv2
import numpy as np

from data_engine.sample import Sample
from data_engine.synthesizers.cutpaste_synthesizer import CutPasteSynthesizer
from data_engine.synthesizers.draem_synthesizer import DRAEMSynthesizer
from data_engine.synthesizers.nsa_synthesizer import NSASynthesizer


def create_synthetic_scene() -> Sample:
    """Creates a mock object image resembling a pill or screw on a clean background."""
    h, w = 256, 256
    img = np.full((h, w, 3), 30, dtype=np.uint8)
    # Draw pill/capsule body
    cv2.ellipse(img, (128, 128), (50, 90), 20, 0, 360, (190, 200, 210), -1)
    cv2.circle(img, (100, 70), 30, (220, 140, 80), -1)
    # Add subtle texture
    noise = np.random.normal(0, 5, (h, w, 3)).astype(np.int16)
    img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    return Sample(
        image=img,
        mask=None,
        category="pill",
        defect_type="good",
        is_anomaly=False,
    )


def overlay_mask_on_image(image: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """Overlays red tint on mask regions."""
    vis = image.copy()
    if mask is not None and np.any(mask > 0):
        red_tint = np.zeros_like(image)
        red_tint[:, :, 0] = 255  # Red channel
        alpha = (mask > 0)[:, :, np.newaxis] * 0.4
        vis = (1.0 - alpha) * vis + alpha * red_tint
        # Draw green contours around mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(vis, contours, -1, (0, 255, 0), 1)
    return np.clip(vis, 0, 255).astype(np.uint8)


def main():
    os.makedirs("results/figures", exist_ok=True)
    sample = create_synthetic_scene()

    synth_cp = CutPasteSynthesizer(mode="scar", scar_width=(4, 10), scar_height=(25, 50), seed=42)
    synth_dr = DRAEMSynthesizer(perlin_threshold=0.35, seed=42)
    synth_nsa = NSASynthesizer(width_ratio_range=(0.1, 0.25), height_ratio_range=(0.1, 0.25), seed=42)

    s_cp = synth_cp(sample)
    s_dr = synth_dr(sample)
    s_nsa = synth_nsa(sample)

    row_orig = sample.image
    row_cp = overlay_mask_on_image(s_cp.image, s_cp.mask)
    row_dr = overlay_mask_on_image(s_dr.image, s_dr.mask)
    row_nsa = overlay_mask_on_image(s_nsa.image, s_nsa.mask)

    # Put text labels on each pane
    for pane, title in zip(
        [row_orig, row_cp, row_dr, row_nsa],
        ["Original Normal", "CutPaste-Scar", "DRAEM-Perlin", "NSA-Poisson"]
    ):
        cv2.putText(pane, title, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    # Combine side-by-side
    canvas = np.hstack([row_orig, row_cp, row_dr, row_nsa])

    out_path = "results/figures/synthetic_preview.png"
    # Convert RGB to BGR for OpenCV saving
    bgr_canvas = cv2.cvtColor(canvas, cv2.COLOR_RGB2BGR)
    cv2.imwrite(out_path, bgr_canvas)
    print(f"Saved visual verification preview to: {out_path}")


if __name__ == "__main__":
    main()
