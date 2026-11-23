"""
Base class for synthetic anomaly generators.
"""

from abc import abstractmethod
from typing import Optional
import random
import numpy as np

from data_engine.base import BaseProcessor
from data_engine.sample import Sample


class BaseSynthesizer(BaseProcessor):
    """
    Abstract base class for all synthetic anomaly generators (Group A).

    Parameters:
        anomaly_prob: Probability of injecting a synthetic anomaly into the sample.
                      If 1.0 (default), always synthesizes an anomaly.
                      If < 1.0, randomly keeps samples defect-free.
        seed: Optional random seed for reproducible synthesis.
    """

    def __init__(
        self,
        anomaly_prob: float = 1.0,
        seed: Optional[int] = None,
        name: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(name=name, **kwargs)
        self.anomaly_prob = float(np.clip(anomaly_prob, 0.0, 1.0))
        self.seed = seed
        self.rng = random.Random(seed)
        if seed is not None:
            np.random.seed(seed)

    def process(self, sample: Sample) -> Sample:
        """
        Executes synthesis based on anomaly_prob.
        If random roll exceeds anomaly_prob, returns cloned original sample (defect-free).
        """
        if self.rng.random() > self.anomaly_prob:
            # Keep sample defect-free
            cloned = sample.clone()
            cloned.is_anomaly = False
            cloned.defect_type = "good"
            cloned.mask = np.zeros(sample.shape[:2], dtype=np.uint8)
            return cloned

        synth_sample = self.synthesize(sample)
        self._validate_synthetic_output(synth_sample)
        return synth_sample

    @abstractmethod
    def synthesize(self, sample: Sample) -> Sample:
        """
        Synthesizes an anomaly on the input sample.
        Must return a new or modified Sample with updated image and binary mask {0, 255}.
        """
        raise NotImplementedError

    def _validate_synthetic_output(self, sample: Sample):
        """Ensures mask is strictly uint8 {0, 255} and spatial dimensions match."""
        h, w = sample.image.shape[:2]
        if sample.mask is None:
            sample.mask = np.zeros((h, w), dtype=np.uint8)
            sample.is_anomaly = False
            return

        mh, mw = sample.mask.shape[:2]
        if (mh, mw) != (h, w):
            raise ValueError(f"Synthetic mask shape {(mh, mw)} does not match image {(h, w)}")

        # Ensure mask is binary uint8 {0, 255}
        if sample.mask.dtype != np.uint8:
            sample.mask = sample.mask.astype(np.uint8)

        # Threshold any values > 0 to 255
        sample.mask[sample.mask > 0] = 255

        has_defect_pixels = bool(np.any(sample.mask > 0))
        sample.is_anomaly = has_defect_pixels
        if has_defect_pixels and sample.defect_type in ("good", ""):
            sample.defect_type = f"synth_{self.name.lower()}"
