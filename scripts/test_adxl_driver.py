from src.drivers.adxl345 import ADXL345
import time

sensor = ADXL345()
sensor.configure(rate_hz=200, range_g=4)

for _ in range(10):
    x, y, z = sensor.read_xyz()
    print(x, y, z)
    time.sleep(0.1)

sensor.close()