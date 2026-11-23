"""
Base interfaces for dataset loaders, processors, exporters, and pipelines.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import time
import logging
from data_engine.sample import Sample

logger = logging.getLogger(__name__)


class BaseProcessor(ABC):
    """
    Abstract base class for all image and mask processing stages
    (enhancers, synthesizers, filters, augmenters, slicers).
    """

    def __init__(self, name: Optional[str] = None, **kwargs):
        self.name = name or self.__class__.__name__
        self.config = kwargs

    def __call__(self, sample: Sample) -> Sample:
        return self.process(sample)

    @abstractmethod
    def process(self, sample: Sample) -> Sample:
        """
        Process a single Sample object. Must return a Sample object
        (either modified in-place, cloned, or newly created).
        """
        raise NotImplementedError

    def process_batch(self, samples: List[Sample]) -> List[Sample]:
        """
        Process a list of samples. Default implementation applies process sequentially.
        Can be overridden for vectorized / multi-threaded batch operations.
        """
        return [self.process(sample) for sample in samples]

    def __repr__(self) -> str:
        return f"{self.name}(config={self.config})"


class BaseDatasetLoader(ABC):
    """
    Abstract base class for industrial anomaly dataset loaders (MVTec AD, VisA, etc.).
    """

    def __init__(self, root_dir: str, **kwargs):
        self.root_dir = root_dir
        self.config = kwargs

    @abstractmethod
    def get_categories(self) -> List[str]:
        """Returns the list of object/texture categories present in the dataset."""
        raise NotImplementedError

    @abstractmethod
    def load(
        self,
        categories: Optional[List[str]] = None,
        split: str = "train",
        **kwargs
    ) -> List[Sample]:
        """
        Loads samples from the dataset.
        Args:
            categories: List of categories to load, or None for all categories.
            split: 'train', 'val', or 'all'.
        """
        raise NotImplementedError


class BaseExporter(ABC):
    """
    Abstract base class for exporting processed samples into model-ready formats
    (YOLO segmentation, COCO JSON, etc.).
    """

    def __init__(self, output_dir: str, **kwargs):
        self.output_dir = output_dir
        self.config = kwargs

    @abstractmethod
    def export(
        self,
        samples: List[Sample],
        split: str = "train",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Export a list of samples to the target directory.
        Returns metadata / summary statistics about the export.
        """
        raise NotImplementedError


class Pipeline:
    """
    Sequential pipeline manager that chains multiple BaseProcessor instances.
    """

    def __init__(self, processors: Optional[List[BaseProcessor]] = None):
        self.processors: List[BaseProcessor] = processors or []

    def add(self, processor: BaseProcessor) -> "Pipeline":
        """Appends a processor to the pipeline."""
        if not isinstance(processor, BaseProcessor):
            raise TypeError(f"Expected BaseProcessor, got {type(processor)}")
        self.processors.append(processor)
        return self

    def run(self, samples: List[Sample]) -> List[Sample]:
        """
        Executes all processors sequentially across the provided samples.
        """
        current_samples = samples
        for idx, proc in enumerate(self.processors):
            start_time = time.time()
            logger.info(f"Running stage [{idx + 1}/{len(self.processors)}]: {proc.name} on {len(current_samples)} samples...")
            current_samples = proc.process_batch(current_samples)
            elapsed = time.time() - start_time
            logger.info(f"Stage {proc.name} completed in {elapsed:.3f}s. Remaining samples: {len(current_samples)}")
        return current_samples

    def __len__(self) -> int:
        return len(self.processors)

    def __repr__(self) -> str:
        stages = " -> ".join([p.name for p in self.processors])
        return f"Pipeline({stages if stages else 'Empty'})"
