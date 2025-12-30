"""
Run continuous real-time inference on ADXL345 using a trained edge ML model.

- Acquires blocks continuously
- Extracts features
- Runs ML inference
- Stops cleanly on Ctrl+C
"""

from src.drivers.adxl345 import ADXL345
from src.sampling.block_sampler import BlockSampler
from src.features.basic_features import BasicStatFeatures
import joblib
import numpy as np
import time

MODEL_PATH = "models/idle_vibration_model.joblib"


def main():
    sensor = ADXL345()
    sensor.configure(rate_hz=200, range_g=4)

    sampler = BlockSampler(sensor, block_size=256)
    extractor = BasicStatFeatures()

    model = joblib.load(MODEL_PATH)

    print("Starting real-time inference. Press Ctrl+C to stop.\n")

    try:
        while True:
            block = sampler.acquire_block()
            features = extractor.extract(block)

            # IMPORTANT: same feature order as training
            feature_keys = sorted(features.keys())
            X = np.array([[features[k] for k in feature_keys]])

            prediction = model.predict(X)[0]

            label = "VIBRATION" if prediction == 1 else "IDLE"
            print(f"Prediction: {label}")

            # Optional: small pause to avoid flooding the terminal
            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\nStopping inference...")

    finally:
        sensor.close()
        print("Sensor closed. Bye.")


if __name__ == "__main__":
    main()
