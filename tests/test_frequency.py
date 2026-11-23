import os
import shutil
import tempfile
import pytest
import numpy as np
import cv2

from data_engine.sample import Sample
from data_engine.frequency.fft_filter import FFTPeriodicSuppressionFilter, compute_butterworth_highpass
from data_engine.frequency.dwt_filter import DWTSubbandFilter, _numpy_haar_dwt2, _numpy_haar_idwt2
from data_engine.exporters.yolo_seg_exporter import YOLOSegExporter


@pytest.fixture
def periodic_grid_sample():
    """Generates a synthetic periodic sinusoidal grid (simulating MVTec 'grid' texture)."""
    h, w = 128, 128
    y, x = np.mgrid[0:h, 0:w]
    freq = 8.0  # 8 cycles across image
    sine_pattern = 128.0 + 80.0 * np.sin(2.0 * np.pi * freq * x / w) * np.cos(2.0 * np.pi * freq * y / h)
    img = np.clip(sine_pattern, 0, 255).astype(np.uint8)
    rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

    # Add a local localized defect (e.g. metal contamination)
    mask = np.zeros((h, w), dtype=np.uint8)
    mask[40:60, 50:75] = 255
    rgb[40:60, 50:75] = 250  # bright stain

    return Sample(
        image=rgb,
        mask=mask,
        category="grid",
        defect_type="metal_contamination",
        is_anomaly=True,
    )


@pytest.fixture
def object_with_mask_sample():
    """Generates a 128x128 object sample with an off-center defect mask."""
    h, w = 128, 128
    img = np.full((h, w, 3), 40, dtype=np.uint8)
    cv2.circle(img, (64, 64), 30, (160, 160, 170), -1)

    mask = np.zeros((h, w), dtype=np.uint8)
    # Triangular defect
    pts = np.array([[50, 40], [70, 40], [60, 65]], np.int32)
    cv2.fillPoly(mask, [pts], 255)
    img[mask > 0] = 230

    return Sample(
        image=img,
        mask=mask,
        category="screw",
        defect_type="thread_damage",
        is_anomaly=True,
    )


class TestFFTPeriodicSuppressionFilter:
    def test_output_shape_and_dtype(self, periodic_grid_sample):
        flt = FFTPeriodicSuppressionFilter(tau=3.0, notch_sigma=3.0)
        out = flt(periodic_grid_sample)

        # 1. Output shape must match input shape exactly
        assert out.shape == periodic_grid_sample.shape
        assert out.image.dtype == np.uint8
        # 2. No NaN or Inf
        assert not np.isnan(out.image).any()
        assert not np.isinf(out.image).any()

    def test_odd_dimensions_handling(self):
        # 127x129 odd-sized image
        img = np.full((127, 129, 3), 100, dtype=np.uint8)
        sample = Sample(image=img, category="tile")
        flt = FFTPeriodicSuppressionFilter()
        out = flt(sample)
        assert out.shape == (127, 129, 3)
        assert out.image.dtype == np.uint8

    def test_periodic_energy_suppression(self, periodic_grid_sample):
        """Verify that periodic grid energy is significantly suppressed by FFT filter."""
        # Measure variance of periodic background (excluding defect area)
        clean_bg_mask = periodic_grid_sample.mask == 0
        var_before = float(np.var(periodic_grid_sample.image[clean_bg_mask]))

        flt = FFTPeriodicSuppressionFilter(tau=2.5, notch_sigma=4.0, dc_radius_ratio=0.03)
        out = flt(periodic_grid_sample)

        var_after = float(np.var(out.image[clean_bg_mask]))
        # The periodic variation must be reduced by at least 30%
        assert var_after < (var_before * 0.70), (
            f"Periodic energy was not suppressed: before={var_before:.2f}, after={var_after:.2f}"
        )

    def test_butterworth_highpass_transfer_function(self):
        h_bw = compute_butterworth_highpass((64, 64), cutoff_ratio=0.1, order=2)
        assert h_bw.shape == (64, 64)
        # DC center (32, 32) should be close to 0
        assert h_bw[32, 32] < 0.05
        # High frequency corners should be close to 1
        assert h_bw[0, 0] > 0.90


class TestDWTSubbandFilter:
    def test_output_shape_and_dtype(self, object_with_mask_sample):
        dwt_flt = DWTSubbandFilter(alpha=0.5, gamma=1.8, wavelet="haar")
        out = dwt_flt(object_with_mask_sample)

        assert out.shape == object_with_mask_sample.shape
        assert out.image.dtype == np.uint8
        assert not np.isnan(out.image).any()
        assert not np.isinf(out.image).any()

    def test_odd_dimensions_handling(self):
        img = np.full((125, 131, 3), 120, dtype=np.uint8)
        sample = Sample(image=img, category="pill")
        dwt_flt = DWTSubbandFilter()
        out = dwt_flt(sample)
        assert out.shape == (125, 131, 3)

    def test_numpy_haar_roundtrip_reconstruction(self):
        """Verify pure NumPy Haar DWT + IDWT achieves near-perfect reconstruction when alpha=gamma=1."""
        x = np.random.uniform(10, 240, (64, 64)).astype(np.float32)
        coeffs = _numpy_haar_dwt2(x)
        recon = _numpy_haar_idwt2(coeffs, (64, 64))
        # Reconstruction error should be minimal
        max_err = float(np.max(np.abs(x - recon)))
        assert max_err < 1e-4

    def test_dwt_detail_boost(self, object_with_mask_sample):
        """Detail amplification (gamma=2.5, alpha=0.2) should enhance edge transitions."""
        dwt_flt = DWTSubbandFilter(alpha=0.2, gamma=2.5)
        out = dwt_flt(object_with_mask_sample)
        assert out.image.dtype == np.uint8
        # Ensure image has valid non-zero content
        assert np.mean(out.image) > 5.0


class TestSpatialAlignmentPreservation:
    def test_mask_alignment_and_yolo_polygons_preserved(self, object_with_mask_sample):
        """
        Verify that frequency domain preprocessing (FFT & DWT) preserves strict
        spatial pixel alignment so YOLO segmentation ground-truth polygon coordinates
        are not offset or distorted.
        """
        fft_flt = FFTPeriodicSuppressionFilter()
        dwt_flt = DWTSubbandFilter()

        s_fft = fft_flt(object_with_mask_sample)
        s_dwt = dwt_flt(object_with_mask_sample)

        # 1. Mask arrays must be bit-exact identical
        assert np.array_equal(s_fft.mask, object_with_mask_sample.mask)
        assert np.array_equal(s_dwt.mask, object_with_mask_sample.mask)

        # 2. Export through YOLOSegExporter and verify polygon coordinates
        tmp_dir = tempfile.mkdtemp()
        try:
            exporter = YOLOSegExporter(output_dir=tmp_dir)
            exporter.export([object_with_mask_sample], split="orig")
            exporter.export([s_fft], split="fft")
            exporter.export([s_dwt], split="dwt")

            with open(os.path.join(tmp_dir, "labels", "orig", "screw_thread_damage_00000.txt"), "r") as f:
                orig_poly = f.read().strip()
            with open(os.path.join(tmp_dir, "labels", "fft", "screw_thread_damage_00000.txt"), "r") as f:
                fft_poly = f.read().strip()
            with open(os.path.join(tmp_dir, "labels", "dwt", "screw_thread_damage_00000.txt"), "r") as f:
                dwt_poly = f.read().strip()

            # Polygon annotations must match exactly
            assert orig_poly == fft_poly
            assert orig_poly == dwt_poly
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)
