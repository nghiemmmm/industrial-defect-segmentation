"""
FAIR Periodic Background Suppression and High-Pass 2D-FFT Filter.
Transforms image to 2D frequency domain (np.fft.fft2, fftshift),
detects and attenuates periodic frequency peaks, and reconstructs spatial RGB via 2D-IFFT.
"""

from typing import Optional, Tuple
import cv2
import numpy as np

from data_engine.base import BaseProcessor
from data_engine.sample import Sample


def compute_butterworth_highpass(
    shape: Tuple[int, int],
    cutoff_ratio: float = 0.05,
    order: int = 2,
) -> np.ndarray:
    """
    Computes a 2D radial Butterworth high-pass transfer function centered at frequency grid origin.
    H(u, v) = 1 / (1 + (D0 / (D(u, v) + eps))^(2 * order))
    """
    h, w = shape
    cy, cx = h / 2.0, w / 2.0
    y = np.arange(h, dtype=np.float32) - cy
    x = np.arange(w, dtype=np.float32) - cx
    xx, yy = np.meshgrid(x, y)
    d = np.sqrt(xx ** 2 + yy ** 2)

    d0 = max(1.0, cutoff_ratio * min(h, w) / 2.0)
    eps = 1e-6
    h_filter = 1.0 / (1.0 + (d0 / (d + eps)) ** (2 * order))
    return h_filter.astype(np.float32)


class FFTPeriodicSuppressionFilter(BaseProcessor):
    """
    FAIR 2D-FFT Periodic Pattern Suppression and High-Pass Preprocessor.

    Parameters:
        tau: Peak detection sensitivity. Peaks in the shifted magnitude spectrum with
             magnitude > tau * median(magnitude) outside the DC radius are suppressed.
        dc_radius_ratio: Fraction of image dimension around (H/2, W/2) protected from notch filtering.
        notch_sigma: Standard deviation (radius) of Gaussian notch attenuation around detected peaks.
        butterworth_cutoff: Optional cutoff ratio for Butterworth high-pass filter.
                            If None, Butterworth filtering is disabled and only notch filtering is applied.
        butterworth_order: Order of the Butterworth transfer function.
        use_luminance: If True (default), processes only the Luminance (Y) channel in YCrCb space,
                       retaining original Cr and Cb chroma channels to prevent color distortion.
    """

    def __init__(
        self,
        tau: float = 4.0,
        dc_radius_ratio: float = 0.05,
        notch_sigma: float = 3.0,
        butterworth_cutoff: Optional[float] = None,
        butterworth_order: int = 2,
        use_luminance: bool = True,
        name: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(name=name or "FFTPeriodicSuppression", **kwargs)
        self.tau = float(tau)
        self.dc_radius_ratio = float(dc_radius_ratio)
        self.notch_sigma = float(notch_sigma)
        self.butterworth_cutoff = butterworth_cutoff
        self.butterworth_order = int(butterworth_order)
        self.use_luminance = bool(use_luminance)

    def _filter_single_channel_2d(self, channel_f32: np.ndarray) -> np.ndarray:
        """
        Applies 2D-FFT -> peak suppression notch & Butterworth -> 2D-IFFT.
        """
        h, w = channel_f32.shape[:2]
        cy, cx = h // 2, w // 2

        # 1. 2D Forward FFT and shift origin to center
        f = np.fft.fft2(channel_f32)
        fshift = np.fft.fftshift(f)
        mag = np.abs(fshift)

        # 2. Distance matrix from DC center (cy, cx)
        y = np.arange(h, dtype=np.float32) - cy
        x = np.arange(w, dtype=np.float32) - cx
        xx, yy = np.meshgrid(x, y)
        dist_from_dc = np.sqrt(xx ** 2 + yy ** 2)

        # 3. Detect periodic frequency peaks (outside DC protected circle)
        dc_radius = max(2.0, self.dc_radius_ratio * min(h, w) / 2.0)
        outside_dc = dist_from_dc > dc_radius

        median_mag = np.median(mag)
        threshold = self.tau * median_mag
        peak_mask = (mag > threshold) & outside_dc

        # 4. Construct Gaussian notch filter to attenuate periodic peaks
        notch_filter = np.ones((h, w), dtype=np.float32)
        peak_coords = np.argwhere(peak_mask)

        # Cap max detected peaks to prevent extreme over-filtering
        max_peaks = 100
        if len(peak_coords) > max_peaks:
            # Sort by peak magnitude descending
            mags = [mag[py, px] for py, px in peak_coords]
            top_indices = np.argsort(mags)[-max_peaks:]
            peak_coords = peak_coords[top_indices]

        for py, px in peak_coords:
            d_sq = (yy - (py - cy)) ** 2 + (xx - (px - cx)) ** 2
            # Attenuate peak with smooth Gaussian notch
            notch_filter *= (1.0 - np.exp(-d_sq / (2.0 * (self.notch_sigma ** 2))))

        f_filtered = fshift * notch_filter

        # 5. Optional Butterworth high-pass filtering
        if self.butterworth_cutoff is not None and self.butterworth_cutoff > 0:
            bw_filter = compute_butterworth_highpass(
                (h, w),
                cutoff_ratio=self.butterworth_cutoff,
                order=self.butterworth_order,
            )
            f_filtered = f_filtered * bw_filter

        # 6. Inverse 2D-FFT and shift back
        f_ishift = np.fft.ifftshift(f_filtered)
        img_recon = np.real(np.fft.ifft2(f_ishift))
        return img_recon

    def process(self, sample: Sample) -> Sample:
        img = sample.image
        h, w = img.shape[:2]

        if self.use_luminance and len(img.shape) == 3 and img.shape[2] == 3:
            # Luminance-domain processing (Y in YCrCb)
            ycrcb = cv2.cvtColor(img, cv2.COLOR_RGB2YCrCb)
            y_chan = ycrcb[:, :, 0].astype(np.float32)
            y_filtered = self._filter_single_channel_2d(y_chan)

            # Preserve dynamic range while preventing clipping artifacts
            y_norm = np.clip(y_filtered, 0, 255).astype(np.uint8)
            ycrcb[:, :, 0] = y_norm
            recon_rgb = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2RGB)
        elif len(img.shape) == 3:
            # Independent per-channel RGB processing
            recon_rgb = np.zeros_like(img, dtype=np.uint8)
            for c in range(img.shape[2]):
                chan = img[:, :, c].astype(np.float32)
                filt = self._filter_single_channel_2d(chan)
                recon_rgb[:, :, c] = np.clip(filt, 0, 255).astype(np.uint8)
        else:
            # Single-channel grayscale
            filt = self._filter_single_channel_2d(img.astype(np.float32))
            recon_rgb = np.clip(filt, 0, 255).astype(np.uint8)

        out_sample = sample.clone()
        out_sample.image = recon_rgb
        # Mask is strictly spatially aligned and preserved
        return out_sample
