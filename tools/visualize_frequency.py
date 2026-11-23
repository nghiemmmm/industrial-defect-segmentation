#!/usr/bin/env python3
"""
Visual verification script for Frequency Domain Preprocessing (Group B).
Generates a side-by-side comparison:
[Original Periodic Grid] -> [FFT Periodic Suppression] -> [2D-DWT Detail Boost]
Saves to results/figures/frequency_preview.png.
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import cv2
import numpy as np

from data_engine.sample import Sample
from data_engine.frequency.fft_filter import FFTPeriodicSuppressionFilter
from data_engine.frequency.dwt_filter import DWTSubbandFilter


def generate_grid_defect_scene() -> Sample:
    h, w = 256, 256
    y, x = np.mgrid[0:h, 0:w]
    freq = 16.0  # Periodic mesh
    sine_mesh = 128.0 + 85.0 * np.sin(2.0 * np.pi * freq * x / w) * np.cos(2.0 * np.pi * freq * y / h)
    img = np.clip(sine_mesh, 0, 255).astype(np.uint8)
    rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

    # Inject a realistic local crack / scratch
    mask = np.zeros((h, w), dtype=np.uint8)
    pts = np.array([[80, 110], [130, 140], [170, 135], [200, 160]], np.int32)
    cv2.polylines(rgb, [pts], isClosed=False, color=(240, 50, 50), thickness=3)
    cv2.polylines(mask, [pts], isClosed=False, color=255, thickness=4)

    return Sample(
        image=rgb,
        mask=mask,
        category="grid",
        defect_type="broken_wire",
        is_anomaly=True,
    )


def main():
    os.makedirs("results/figures", exist_ok=True)
    sample = generate_grid_defect_scene()

    fft_flt = FFTPeriodicSuppressionFilter(tau=2.5, notch_sigma=4.0, dc_radius_ratio=0.03)
    dwt_flt = DWTSubbandFilter(alpha=0.3, gamma=2.2, wavelet="haar")

    s_fft = fft_flt(sample)
    s_dwt = dwt_flt(sample)

    pane_orig = sample.image.copy()
    pane_fft = s_fft.image.copy()
    pane_dwt = s_dwt.image.copy()

    for pane, title in zip(
        [pane_orig, pane_fft, pane_dwt],
        ["Original Grid Texture", "FAIR FFT Periodic Suppressed", "2D-DWT Detail Boosted"]
    ):
        cv2.putText(pane, title, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2)

    canvas = np.hstack([pane_orig, pane_fft, pane_dwt])
    out_path = "results/figures/frequency_preview.png"
    bgr_canvas = cv2.cvtColor(canvas, cv2.COLOR_RGB2BGR)
    cv2.imwrite(out_path, bgr_canvas)
    print(f"Saved frequency domain preview to: {out_path}")


if __name__ == "__main__":
    main()
