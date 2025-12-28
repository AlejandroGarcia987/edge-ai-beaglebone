from src.drivers.adxl345 import ADXL345
from src.sampling.block_sampler import BlockSampler

sensor = ADXL345()
sensor.configure(rate_hz=200, range_g=4)

sampler = BlockSampler(sensor, fs_hz=200, block_size=256)

block = sampler.acquire_block()
print(block.shape)
print(block[:5])

sensor.close()