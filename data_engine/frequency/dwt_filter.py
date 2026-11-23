"""
2D Discrete Wavelet Transform (2D-DWT) Sub-band Filter.
Based on WE-PaDiM and multi-resolution frequency analysis for industrial defect detection.
Decomposes input into (LL, LH, HL, HH) sub-bands, applies selective low-frequency
attenuation and high-frequency edge amplification, and reconstructs spatial RGB via 2D-IDWT.
"""

from typing import Optional, Tuple
import cv2
import numpy as np

from data_engine.base import BaseProcessor
from data_engine.sample import Sample

try:
    import pywt
    HAS_PYWT = True
except ImportError:
    HAS_PYWT = False


def _numpy_haar_dwt2(x: np.ndarray) -> Tuple[np.ndarray, Tuple[np.ndarray, np.ndarray, np.ndarray]]:
    """
    Pure NumPy fallback for 2D Haar Discrete Wavelet Transform.
    """
    h, w = x.shape[:2]
    # Ensure even dimensions
    if h % 2 != 0:
        x = np.pad(x, ((0, 1), (0, 0)), mode="reflect")
    if w % 2 != 0:
        x = np.pad(x, ((0, 0), (0, 1)), mode="reflect")

    # 1D Haar along columns
    l = (x[0::2, :] + x[1::2, :]) / math.sqrt(2.0)
    h_sub = (x[0::2, :] - x[1::2, :]) / math.sqrt(2.0)

    # 1D Haar along rows
    ll = (l[:, 0::2] + l[:, 1::2]) / math.sqrt(2.0)
    lh = (l[:, 0::2] - l[:, 1::2]) / math.sqrt(2.0)
    hl = (h_sub[:, 0::2] + h_sub[:, 1::2]) / math.sqrt(2.0)
    hh = (h_sub[:, 0::2] - h_sub[:, 1::2]) / math.sqrt(2.0)

    return ll, (lh, hl, hh)


def _numpy_haar_idwt2(coeffs: Tuple[np.ndarray, Tuple[np.ndarray, np.ndarray, np.ndarray]], target_shape: Tuple[int, int]) -> np.ndarray:
    """
    Pure NumPy fallback for 2D Haar Inverse Discrete Wavelet Transform.
    """
    ll, (lh, hl, hh) = coeffs
    # Inverse 1D Haar along rows
    l = np.zeros((ll.shape[0], ll.shape[1] * 2), dtype=np.float32)
    l[:, 0::2] = (ll + lh) / math.sqrt(2.0)
    l[:, 1::2] = (ll - lh) / math.sqrt(2.0)

    h_sub = np.zeros((hl.shape[0], hl.shape[1] * 2), dtype=np.float32)
    h_sub[:, 0::2] = (hl + hh) / math.sqrt(2.0)
    h_sub[:, 1::2] = (hl - hh) / math.sqrt(2.0)

    # Inverse 1D Haar along columns
    out = np.zeros((l.shape[0] * 2, l.shape[1]), dtype=np.float32)
    out[0::2, :] = (l + h_sub) / math.sqrt(2.0)
    out[1::2, :] = (l - h_sub) / math.sqrt(2.0)

    return out[:target_shape[0], :target_shape[1]]


import math


class DWTSubbandFilter(BaseProcessor):
    """
    2D Discrete Wavelet Transform (2D-DWT) Sub-band Preprocessor.

    Decomposes image into:
        LL: Low-frequency approximation (smooth background illumination).
        LH: Horizontal high-frequency details (vertical edges/defects).
        HL: Vertical high-frequency details (horizontal edges/defects).
        HH: Diagonal high-frequency details (corners/fine texture anomalies).

    Transformation applied:
        LL_tilde = alpha * LL
        LH_tilde = gamma * LH
        HL_tilde = gamma * HL
        HH_tilde = gamma * HH
        Output = IDWT2((LL_tilde, (LH_tilde, HL_tilde, HH_tilde)))

    Parameters:
        alpha: Attenuation factor for low-frequency LL sub-band (e.g. 0.5 to suppress smooth background).
        gamma: Amplification factor for high-frequency detail sub-bands (e.g. 1.5 to boost crack/scratch edges).
        wavelet: Wavelet family (e.g. 'haar', 'db2', 'bior1.3').
        use_luminance: If True, applies DWT exclusively to Luminance (Y) channel in YCrCb space.
    """

    def __init__(
        self,
        alpha: float = 0.6,
        gamma: float = 1.5,
        wavelet: str = "haar",
        use_luminance: bool = True,
        name: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(name=name or "DWTSubbandFilter", **kwargs)
        self.alpha = float(alpha)
        self.gamma = float(gamma)
        self.wavelet = str(wavelet)
        self.use_luminance = bool(use_luminance)

    def _filter_single_channel_2d(self, channel_f32: np.ndarray) -> np.ndarray:
        h, w = channel_f32.shape[:2]

        if HAS_PYWT:
            # 2D-DWT decomposition via PyWavelets
            coeffs = pywt.dwt2(channel_f32, self.wavelet, mode="symmetric")
            ll, (lh, hl, hh) = coeffs

            # Apply attenuation and amplification
            ll_mod = ll * self.alpha
            lh_mod = lh * self.gamma
            hl_mod = hl * self.gamma
            hh_mod = hh * self.gamma

            # 2D-IDWT reconstruction
            recon = pywt.idwt2((ll_mod, (lh_mod, hl_mod, hh_mod)), self.wavelet, mode="symmetric")
            # Crop to original spatial dimensions in case of odd-dimension boundary padding
            recon = recon[:h, :w]
        else:
            # Pure NumPy Haar DWT fallback
            ll, (lh, hl, hh) = _numpy_haar_dwt2(channel_f32)
            ll_mod = ll * self.alpha
            lh_mod = lh * self.gamma
            hl_mod = hl * self.gamma
            hh_mod = hh * self.gamma
            recon = _numpy_haar_idwt2((ll_mod, (lh_mod, hl_mod, hh_mod)), (h, w))

        return recon

    def process(self, sample: Sample) -> Sample:
        img = sample.image
        h, w = img.shape[:2]

        if self.use_luminance and len(img.shape) == 3 and img.shape[2] == 3:
            # Process strictly in Luminance domain (Y in YCrCb)
            ycrcb = cv2.cvtColor(img, cv2.COLOR_RGB2YCrCb)
            y_chan = ycrcb[:, :, 0].astype(np.float32)
            y_filtered = self._filter_single_channel_2d(y_chan)

            y_norm = np.clip(y_filtered, 0, 255).astype(np.uint8)
            ycrcb[:, :, 0] = y_norm
            recon_rgb = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2RGB)
        elif len(img.shape) == 3:
            recon_rgb = np.zeros_like(img, dtype=np.uint8)
            for c in range(img.shape[2]):
                chan = img[:, :, c].astype(np.float32)
                filt = self._filter_single_channel_2d(chan)
                recon_rgb[:, :, c] = np.clip(filt, 0, 255).astype(np.uint8)
        else:
            filt = self._filter_single_channel_2d(img.astype(np.float32))
            recon_rgb = np.clip(filt, 0, 255).astype(np.uint8)

        out_sample = sample.clone()
        out_sample.image = recon_rgb
        # Mask is strictly spatially aligned and preserved
        return out_sample
