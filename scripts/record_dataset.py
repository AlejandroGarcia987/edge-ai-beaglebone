"""
Record labeled feature dataset from ADXL345.

Usage examples:
  Idle:
    python3 -m scripts.record_dataset --label 0 --blocks 200

  Vibration:
    python3 -m scripts.record_dataset --label 1 --blocks 200
"""

import time
import csv
import argparse

from src.drivers.adxl345 import ADXL345
from src.sampling.block_sampler import BlockSampler
from src.features.basic_features import BasicStatFeatures


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", type=int, required=True, help="Class label (0=idle, 1=vibration)")
    parser.add_argument("--blocks", type=int, default=100, help="Number of blocks to record")
    parser.add_argument("--outfile", type=str, default="data/dataset.csv")
    args = parser.parse_args()

    SAMPLE_RATE_HZ = 200
    BLOCK_SIZE = 256

    sensor = ADXL345()
    sensor.configure(rate_hz=SAMPLE_RATE_HZ, range_g=4)

    sampler = BlockSampler(sensor, block_size=BLOCK_SIZE)
    extractor = BasicStatFeatures()

    print(f"Recording {args.blocks} blocks with label={args.label}")

    with open(args.outfile, "a", newline="") as f:
        writer = csv.writer(f)

        for i in range(args.blocks):
            block = sampler.acquire_block()
            features = extractor.extract(block)

            row = [
                time.time(),
                features["rms_x"], features["rms_y"], features["rms_z"],
                features["mean_x"], features["mean_y"], features["mean_z"],
                features["std_x"], features["std_y"], features["std_z"],
                features["rms_mag"], features["std_mag"],
                args.label,
            ]

            writer.writerow(row)

            print(f"Block {i+1}/{args.blocks}")

    sensor.close()
    print("Done.")


if __name__ == "__main__":
    main()