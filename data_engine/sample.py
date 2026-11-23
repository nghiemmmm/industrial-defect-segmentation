from dataclasses import dataclass, field
from typing import Optional, Dict, Any, Tuple
import numpy as np


@dataclass
class Sample:
    """
    Standard data object representing a single industrial inspection sample.

    Attributes:
        image: np.ndarray (H, W, 3) in RGB uint8 or (H, W) grayscale uint8.
        mask: Optional[np.ndarray] (H, W) binary mask in uint8 (255 for defect, 0 for normal).
              If None or all zeros, the sample is defect-free.
        category: Category of the object (e.g. 'bottle', 'cable', 'transistor').
        defect_type: Defect subtype (e.g. 'broken_large', 'scratch', or 'good').
        is_anomaly: True if the sample contains defect(s), False if it is normal/defect-free.
        image_path: Source file path or identifier for traceability.
        metadata: Arbitrary dictionary for additional context (original size, split, slice coords).
    """
    image: np.ndarray
    mask: Optional[np.ndarray] = None
    category: str = "unknown"
    defect_type: str = "good"
    is_anomaly: bool = False
    image_path: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.image is None or not isinstance(self.image, np.ndarray):
            raise ValueError("Sample image must be a valid numpy ndarray.")
        
        # Ensure mask shape matches image spatial dimensions if present
        if self.mask is not None:
            if not isinstance(self.mask, np.ndarray):
                raise ValueError("Sample mask must be a numpy ndarray if provided.")
            h, w = self.image.shape[:2]
            mh, mw = self.mask.shape[:2]
            if (h, w) != (mh, mw):
                raise ValueError(f"Image shape {(h, w)} and mask shape {(mh, mw)} do not match.")
            # If mask has values > 0 and is_anomaly is False, auto-mark is_anomaly = True
            if np.any(self.mask > 0):
                self.is_anomaly = True
        elif self.is_anomaly is False and self.mask is None:
            # Create a zero-filled mask matching the image dimensions
            h, w = self.image.shape[:2]
            self.mask = np.zeros((h, w), dtype=np.uint8)

    @property
    def shape(self) -> Tuple[int, ...]:
        return self.image.shape

    @property
    def height(self) -> int:
        return self.image.shape[0]

    @property
    def width(self) -> int:
        return self.image.shape[1]

    def has_mask(self) -> bool:
        """Returns True if mask exists and contains at least one non-zero defect pixel."""
        return bool(self.mask is not None and bool(np.any(self.mask > 0)))

    def defect_area_ratio(self) -> float:
        """Returns the ratio of defect pixels to total image pixels."""
        if not self.has_mask():
            return 0.0
        defect_pixels = np.count_nonzero(self.mask > 0)
        total_pixels = self.height * self.width
        return float(defect_pixels / total_pixels) if total_pixels > 0 else 0.0

    def clone(self) -> "Sample":
        """Returns a deep copy of this sample."""
        return Sample(
            image=np.copy(self.image),
            mask=np.copy(self.mask) if self.mask is not None else None,
            category=self.category,
            defect_type=self.defect_type,
            is_anomaly=self.is_anomaly,
            image_path=self.image_path,
            metadata=self.metadata.copy(),
        )

    def summary(self) -> str:
        mask_status = f"defect_area={self.defect_area_ratio():.4%}" if self.has_mask() else "defect_free"
        return (
            f"Sample(category='{self.category}', defect='{self.defect_type}', "
            f"anomaly={self.is_anomaly}, shape={self.shape}, {mask_status})"
        )
