from smbus2 import SMBus, i2c_msg
import time

# I2C setup
bus = SMBus(0)  # Use 0 for I2C0 on Orange Pi 3 LTS

# BH1750 address
address_bh1750 = 0x23

# Function to read the BH1750 (light sensor)
def get_lux(bus, address):
    write = i2c_msg.write(address, [0x10])  # 0x10 = Continuous high resolution mode
    bus.i2c_rdwr(write)
    
    # Read 2 bytes of data
    read = i2c_msg.read(address, 2)
    bus.i2c_rdwr(write, read)
    
    bytes_read = list(read)
    
    # Convert to lux (using the sensor's conversion formula)
    lux = ((bytes_read[0] << 8) + bytes_read[1]) / 1.2  # Conversion factor for BH1750
    return lux

# Main loop to read the BH1750 data and print it
while True:
    try:
        lux = get_lux(bus, address_bh1750)
        print(f"Light intensity: {lux:.2f} lux")
    except Exception as e:
        print(f"Error: {e}")
    
    time.sleep(1)
