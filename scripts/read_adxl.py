from smbus2 import SMBus
import struct

I2C_BUS = 2
ADXL345_ADDRESS = 0x53
REG_DEVID = 0x00
REG_POWER_CTL = 0x2D
REG_DATAX0 = 0x32

with SMBus(I2C_BUS) as bus:
    device_id = bus.read_byte_data(ADXL345_ADDRESS, REG_DEVID)
    print(f"ADXL345 Device ID: {device_id:#04x}")

    if device_id == 0xE5:
        print("ADXL345 detected successfully.")
    else:
        print("Failed to detect ADXL345.")

    # Set the device to measurement mode
    bus.write_byte_data(ADXL345_ADDRESS, REG_POWER_CTL, 0x08)
    print("ADXL345 set to measurement mode.")

    # Read acceleration data
    data = bus.read_i2c_block_data(ADXL345_ADDRESS, REG_DATAX0, 6)
    x, y, z = struct.unpack('<hhh', bytes(data))
    print(f"Acceleration Data - X: {x}, Y: {y}, Z: {z}")
