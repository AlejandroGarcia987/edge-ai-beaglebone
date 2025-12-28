from src.drivers.adxl345 import ADXL345
from src.sampling.timing_sampler import TimingSampler

sensor = ADXL345()
sensor.configure(rate_hz=200, range_g=4)

sampler = TimingSampler(sensor, target_hz=200)
sampler.run(num_samples=500)

stats = sampler.timing_stats()

print("Timing statistics:")
for k, v in stats.items():
    print(f"{k:20s}: {v:.4f}")

sensor.close()
