from smbus2 import SMBus
import struct

class ADXL345:
    ADDRESS = 0x53

    REG_DEVID = 0x00
    REG_BW_RATE = 0x2C
    REG_POWER_CTL = 0x2D
    REG_DATA_FORMAT = 0x31
    REG_DATAX0 = 0x32
    REG_FIFO_CTL = 0x38

    DEVICE_ID = 0xE5

    def __init__(self, bus_id=2):
        self.bus = SMBus(bus_id)
        self._check_device()

    def _check_device(self):
        devid = self.bus.read_byte_data(self.ADDRESS, self.REG_DEVID)
        if devid != self.DEVICE_ID:
            raise RuntimeError(f"ADXL345 not detected (got {hex(devid)})")

    def configure(self, rate_hz=200, range_g=4):
        # BW_RATE
        rate_map = {
            100: 0x0A,
            200: 0x0B,
            400: 0x0C,
        }
        self.bus.write_byte_data(self.ADDRESS, self.REG_BW_RATE, rate_map[rate_hz])

        # DATA_FORMAT: FULL_RES + range
        range_map = {2: 0x00, 4: 0x01, 8: 0x02, 16: 0x03}
        data_format = (1 << 3) | range_map[range_g]
        self.bus.write_byte_data(self.ADDRESS, self.REG_DATA_FORMAT, data_format)

        # FIFO: stream mode, 32 samples
        self.bus.write_byte_data(self.ADDRESS, self.REG_FIFO_CTL, 0xA0)

        # Measurement mode
        self.bus.write_byte_data(self.ADDRESS, self.REG_POWER_CTL, 0x08)

    def read_xyz(self):
        data = self.bus.read_i2c_block_data(self.ADDRESS, self.REG_DATAX0, 6)
        return struct.unpack('<hhh', bytes(data))

    def close(self):
        self.bus.close()