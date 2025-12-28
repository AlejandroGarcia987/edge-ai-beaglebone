# check how regular is the sampling timing


"""
Timing and jitter characterization under Linux (BeagleBone).

This module is intentionally included to *measure* and *document* the real
sampling behavior when acquiring sensor data from user space under Linux.

Context
-------
Sampling is performed from Python on a BeagleBone running Linux, without
real-time extensions. Even when using a fixed target sampling frequency
(e.g. 200 Hz, 5 ms period), Linux does NOT guarantee deterministic timing.

For this reason, before building any feature extraction or ML pipeline,
we explicitly measure the real timing behavior instead of assuming an
ideal sampling rate.

Measured example (200 Hz target)
--------------------------------
Typical results obtained on this platform:

    target_period_ms : 5.0000
    mean_period_ms   : ~5.0003
    std_jitter_ms    : ~0.15
    min_period_ms    : ~3.6
    max_period_ms    : ~6.5
    max_error_ms     : ~1.5

Interpretation
--------------
- The *mean period* is very close to the target → no long-term drift.
- There is low average jitter, but clear worst-case deviations.
- Linux occasionally delays or advances execution due to scheduling,
  interrupts, or other system activity.
- Worst-case timing error is ~30% of the nominal period at 200 Hz.

Design decision
---------------
This confirms that:
- Hard real-time assumptions are NOT valid in this setup.
- Deterministic control loops should not rely on this timing.
- Block-based processing, feature extraction, and edge-ML pipelines
  are still perfectly valid when:
    - Using timestamps instead of assuming fixed Fs
    - Operating on windows/statistical features
    - Avoiding per-sample real-time constraints

This measurement justifies the use of:
- Block-based buffering
- Timestamp-aware processing
- Feature-level ML instead of sample-level control

The goal is not to eliminate jitter, but to design the pipeline to be
robust against it.
"""



import time
import numpy as np 

class TimingSampler:
    """
    Measures real sampling timing and jitter under Linux.

    It samples the sensor at a target frequency and records
    per-sample timestamps to analyze timing stability.
    """
    def __init__(self, sensor, target_hz = 200):
        self.sensor = sensor
        self.target_hz = target_hz
        self.period_s = 1.0 / target_hz

        self.timestamps = []
        self.samples = []

    def run(self, num_samples = 500):
        """
        Run the sampler for a fixed number of samples
        """

        self.timestamps.clear()
        self.samples.clear()

        next_time = time.perf_counter()

        for _ in range(num_samples):
            now = time.perf_counter()
            self.timestamps.append(now)

            x, y, z = self.sensor.read_xyz()
            self.samples.append((x, y, z))

            next_time += self.period_s
            sleep_time = next_time - time.perf_counter()
            if sleep_time > 0:
                time.sleep(sleep_time)

        return np.array(self.timestamps), np.array(self.samples)

    def timing_stats(self):
        """
        Compute timing statistics from collected timestamps.
        """
        if len(self.timestamps) < 2:
            raise RuntimeError("Not enough samples collected")

        ts = np.array(self.timestamps)
        deltas = np.diff(ts)

        stats = {
            "target_period_ms": self.period_s * 1000,
            "mean_period_ms": np.mean(deltas) * 1000,
            "std_jitter_ms": np.std(deltas) * 1000,
            "min_period_ms": np.min(deltas) * 1000,
            "max_period_ms": np.max(deltas) * 1000,
            "max_error_ms": np.max(np.abs(deltas - self.period_s)) * 1000,
        }

        return stats


