import time
from smbus2 import SMBus, i2c_msg

# I2C setup (use I2C0 bus)
bus = SMBus(0)  # Use 0 for I2C0 on Orange Pi 3 LTS

# BMP280 address
address_bmp280 = 0x77 # Default address for BMP280

# Function to read temperature from BMP280
def get_temperature(bus, address):
    # BMP280 initialization sequence (write control register)
    # 0xF4 is the control register (settings for the sensor)
    # 0x2F = 0b00101111, Normal mode, temperature and pressure
    write = i2c_msg.write(address, [0xF4, 0x2F])
    bus.i2c_rdwr(write)

    # Wait for the sensor to take a reading
    time.sleep(0.1)

    # Read the raw temperature data (3 bytes: 0xFA, 0xFB, 0xFC)
    read = i2c_msg.read(address, 3)
    bus.i2c_rdwr(write, read)
    
    # Convert the raw data into temperature (temperature is 20-bit value)
    bytes_read = list(read)
    raw_temp = ((bytes_read[0] << 12) | (bytes_read[1] << 4) | (bytes_read[2] >> 4))

    # BMP280 temperature formula (based on datasheet)
    # The temperature is scaled by 5120 (1/5120 degrees per LSB)
    temperature = raw_temp / 5120.0

    return temperature

# Main loop to read temperature and print it
while True:
    try:
        # Get temperature
        temperature = get_temperature(bus, address_bmp280)
        
        # Print the result
        print(f"Temperature: {temperature:.2f}°C")
        
    except Exception as e:
        print(f"Error: {e}")
    
    time.sleep(1)
