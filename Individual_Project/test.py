import time
import os
import requests
from smbus2 import SMBus, i2c_msg
import wiringpi

# Configuration
THINGSPEAK_API_KEY = "1A8WQET2BFB6V6QJ"
THINGSPEAK_URL = "https://api.thingspeak.com/update"
I2C_BUS = 0
BMP280_ADDRESS = 0x77
BH1750_ADDRESS = 0x23
LED_PIN = 3
HEATER_RELAY_PIN = 5
BUTTON_PINS = [7, 8, 11, 12]  # [Temp Up, Temp Down, Lux Up, Lux Down]

# Initialize hardware
wiringpi.wiringPiSetup()
wiringpi.softPwmCreate(LED_PIN, 0, 100)
wiringpi.pinMode(HEATER_RELAY_PIN, 1)

# Set button pins as input with pull-up resistors
for pin in BUTTON_PINS:
    wiringpi.pinMode(pin, 0)  # INPUT
    wiringpi.pullUpDnControl(pin, wiringpi.PUD_UP)

def read_light_sensor(bus):
    try:
        bus.i2c_rdwr(i2c_msg.write(BH1750_ADDRESS, [0x10]))  # Set high-resolution mode
        time.sleep(0.2)
        
        read_msg = i2c_msg.read(BH1750_ADDRESS, 2)
        bus.i2c_rdwr(read_msg)
        
        bytes_read = list(read_msg)
        lux = ((bytes_read[0] << 8) + bytes_read[1]) / 1.2
        return round(lux, 2)
    except Exception as e:
        print(f"Error reading light sensor: {e}")
        return None

def read_temp_sensor(bus):
    try:
        # Initialize sensor - normal mode with 1x oversampling
        bus.write_byte_data(BMP280_ADDRESS, 0xF4, 0x27)
        time.sleep(0.1)
        
        # Read raw temperature data
        raw_temp = bus.read_i2c_block_data(BMP280_ADDRESS, 0xFA, 3)
        raw_temp = ((raw_temp[0] << 12) | (raw_temp[1] << 4) | (raw_temp[2] >> 4))
        
        # Read calibration parameters
        cal_params = bus.read_i2c_block_data(BMP280_ADDRESS, 0x88, 6)
        
        # Calculate temperature using calibration coefficients
        dig_T1 = (cal_params[1] << 8) | cal_params[0]
        dig_T2 = (cal_params[3] << 8) | cal_params[2]
        dig_T3 = (cal_params[5] << 8) | cal_params[4]
        
        # Apply calibration
        var1 = ((raw_temp / 16384.0) - (dig_T1 / 1024.0)) * dig_T2
        var2 = ((raw_temp / 131072.0) - (dig_T1 / 8192.0)) * ((raw_temp / 131072.0) - (dig_T1 / 8192.0)) * dig_T3
        temperature = (var1 + var2) / 5120.0
        
        return round(temperature, 2)
    except Exception as e:
        print(f"Error reading temperature sensor: {e}")
        return None

def update_thingspeak(data):
    params = {'api_key': THINGSPEAK_API_KEY}
    params.update({field: value for field, value in data.items() if value is not None})
    
    try:
        response = requests.get(THINGSPEAK_URL, params=params)
        if response.ok:
            print(f"Data successfully sent to ThingSpeak")
            return True
        else:
            print(f"Error sending to ThingSpeak: {response.status_code}")
            return False
    except Exception as e:
        print(f"ThingSpeak error: {e}")
        return False

def adjust_led_brightness(goal_lux):
    brightness = max(0, min(100, (goal_lux / 353.3) * 100))
    wiringpi.softPwmWrite(LED_PIN, int(brightness))

def control_heating(goal_temp, current_temp):
    if current_temp is not None:
        if current_temp < goal_temp:
            wiringpi.digitalWrite(HEATER_RELAY_PIN, 0)  # ON
            print(f"Heating ON: {current_temp}°C < {goal_temp}°C")
        else:
            wiringpi.digitalWrite(HEATER_RELAY_PIN, 1)  # OFF
            print(f"Heating OFF: {current_temp}°C >= {goal_temp}°C")
    else:
        wiringpi.digitalWrite(HEATER_RELAY_PIN, 1)  # OFF
        print("No temperature data, heater off")

def check_buttons(goal_temp, goal_lux):
    # Check buttons to adjust goals
    if wiringpi.digitalRead(BUTTON_PINS[0]) == wiringpi.LOW:  # Temp Up
        goal_temp += 1
        print(f"Temperature goal: {goal_temp}°C")
        
    if wiringpi.digitalRead(BUTTON_PINS[1]) == wiringpi.LOW:  # Temp Down
        goal_temp -= 1
        print(f"Temperature goal: {goal_temp}°C")
        
    if wiringpi.digitalRead(BUTTON_PINS[2]) == wiringpi.LOW:  # Lux Up
        goal_lux += 1
        adjust_led_brightness(goal_lux)
        print(f"Light goal: {goal_lux} lux")
        
    if wiringpi.digitalRead(BUTTON_PINS[3]) == wiringpi.LOW:  # Lux Down
        goal_lux -= 1
        adjust_led_brightness(goal_lux)
        print(f"Light goal: {goal_lux} lux")
    
    return goal_temp, goal_lux

def main():
    # Initialize hardware
    bus = SMBus(I2C_BUS)
    last_send_time = time.time()
    send_interval = 10  # seconds
    
    # Get initial sensor values to set as goals
    goal_temp = read_temp_sensor(bus) if read_temp_sensor(bus) is not None else 0
    goal_lux = read_light_sensor(bus) if read_light_sensor(bus) is not None else 0
    
    print("=== Sensor Control ===")
    print("Use buttons to adjust temperature and light goals")
    
    try:
        while True:
            # Check for button presses and update goals
            goal_temp, goal_lux = check_buttons(goal_temp, goal_lux)
            
            # Read sensors
            temp = read_temp_sensor(bus)
            light = read_light_sensor(bus)
            
            # Display current readings
            os.system('clear')
            print("=== SENSOR READINGS ===")
            print(f"Temperature: {temp}°C (Goal: {goal_temp}°C)")
            print(f"Light: {light} lux (Goal: {goal_lux} lux)")
            
            # Send data to ThingSpeak every 10 seconds
            current_time = time.time()
            if current_time - last_send_time >= send_interval:
                last_send_time = current_time
                update_thingspeak({
                    'field1': temp, 
                    'field2': light, 
                    'field3': goal_temp, 
                    'field4': goal_lux
                })
            
            # Control devices
            adjust_led_brightness(goal_lux)
            control_heating(goal_temp, temp)
            
            time.sleep(0.1)  # Small delay to prevent CPU overuse
            
    except KeyboardInterrupt:
        print("\nStopped by user")
    finally:
        bus.close()
        wiringpi.digitalWrite(HEATER_RELAY_PIN, 1)  # Turn off heater
        wiringpi.softPwmWrite(LED_PIN, 0)  # Turn off LED
        print("Cleanup completed")

if __name__ == "__main__":
    main()