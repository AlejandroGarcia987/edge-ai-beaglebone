import time 
import numpy as np 

class BlockSampler:
    def __init__(self, sensor, fs_hz = 200, block_size = 256):
        self.sensor = sensor
        self.fs = fs_hz
        self.dt = 1.0 / fs_hz
        self.block_size = block_size
    
    def acquire_block(self):
        block = np.zeros((self.block_size, 3))
        t_next = time.perf_counter()

        for i in range(self.block_size):
            x, y, z = self.sensor.read_xyz()
            block[i] = [x, y, z]

            t_next += self.dt
            sleep_time = t_next - time.perf_counter()
            if sleep_time > 0:
                time.sleep(sleep_time)
        return block
            