import numpy as np
from .base import FeatureExtractor

class BasicStatFeatures(FeatureExtractor):
    """
    Computes basic statistical features per axis and magnitude.
    """

    def extract(self, block: np.ndarray) -> dict:
        features = {}

        x = block[:, 0]
        y = block[:, 1]
        z = block[:, 2]

        # Per-axis RMS
        features["rms_x"] = np.sqrt(np.mean(x**2))
        features["rms_y"] = np.sqrt(np.mean(y**2))
        features["rms_z"] = np.sqrt(np.mean(z**2))

        # Per-axis mean
        features["mean_x"] = np.mean(x)
        features["mean_y"] = np.mean(y)
        features["mean_z"] = np.mean(z)

        # Per-axis std
        features["std_x"] = np.std(x)
        features["std_y"] = np.std(y)
        features["std_z"] = np.std(z)

        # Vector magnitude
        mag = np.sqrt(x**2 + y**2 + z**2)
        features["rms_mag"] = np.sqrt(np.mean(mag**2))
        features["std_mag"] = np.std(mag)

        return features