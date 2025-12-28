from abc import ABC, abstractmethod
import numpy as np

class FeatureExtractor(ABC):
    """
    Base interface for block-based feature extractors.

    Input:
        block: np.ndarray of shape (N, 3)

    Output:
        dict[str, float]
    """

    @abstractmethod
    def extract(self, block: np.ndarray) -> dict:
        pass
