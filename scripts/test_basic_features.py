"""
Test script for basic feature extraction on ADXL345 data.

This script:
- Acquires a block of accelerometer samples
- Extracts basic statistical features
- Prints them for inspection

Intended for:
- Validating feature extraction
- Gaining intuition about sensor data
- Serving as a reference example
"""

from src.drivers.adxl345 import ADXL345
from src.sampling.block_sampler import BlockSampler
from src.features.basic_features import BasicStatFeatures


def main():
    # --- Configuration ---
    SAMPLE_RATE_HZ = 200
    BLOCK_SIZE = 256

    # --- Initialize hardware ---
    sensor = ADXL345()
    sensor.configure(rate_hz=SAMPLE_RATE_HZ, range_g=4)

    # --- Sampling ---
    sampler = BlockSampler(
        sensor=sensor,
        block_size=BLOCK_SIZE,
    )

    print("Collecting one block of accelerometer data...")
    block = sampler.acquire_block()

    # --- Feature extraction ---
    extractor = BasicStatFeatures()
    features = extractor.extract(block)

    # --- Output ---
    print("\nExtracted features:")
    for k, v in features.items():
        print(f"{k:12s}: {v:8.3f}")

    sensor.close()


if __name__ == "__main__":
    main()
