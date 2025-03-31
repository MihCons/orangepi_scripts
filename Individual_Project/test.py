import time
import os
import paho.mqtt.client as mqtt
from smbus2 import SMBus, i2c_msg
import wiringpi

# MQTT Configuration
MQTT_HOST = "mqtt3.thingspeak.com"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 60
MQTT_TOPIC = "channels/2898460/publish"  # Replace with your ThingSpeak channel details
MQTT_CLIENT_ID = "MSgnIBw4IhMFAQ8fOgMRCRs"
MQTT_USER = "MSgnIBw4IhMFAQ8fOgMRCRs"
MQTT_PWD = "OX/hTI1t6r2utzp/gRhBHYus"

# I2C Configuration
I2C_BUS = 0
BMP280_ADDRESS = 0x77
BH1750_ADDRESS = 0x23

# GPIO Configuration
LED_PIN = 3
HEATER_RELAY_PIN = 5
BUTTON_PINS = [7, 8, 11, 12]  # [Temp Up, Temp Down, Lux Up, Lux Down]

# Initialize hardware
wiringpi.wiringPiSetup()
wiringpi.softPwmCreate(LED_PIN, 0, 100)
wiringpi.pinMode(HEATER_RELAY_PIN, 1)

for pin in BUTTON_PINS:
    wiringpi.pinMode(pin, 0)
    wiringpi.pullUpDnControl(pin, wiringpi.PUD_UP)

# MQTT Client Setup
client = mqtt.Client(MQTT_CLIENT_ID)
client.username_pw_set(MQTT_USER, MQTT_PWD)

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to MQTT Broker")
    else:
        print(f"Failed to connect, return code {rc}")

def on_disconnect(client, userdata, flags, rc=0):
    print(f"Disconnected, result code {rc}")

client.on_connect = on_connect
client.on_disconnect = on_disconnect
print(f"Connecting to MQTT Broker at {MQTT_HOST}...")
client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
client.loop_start()

def read_light_sensor(bus):
    try:
        bus.i2c_rdwr(i2c_msg.write(BH1750_ADDRESS, [0x10]))
        time.sleep(0.2)
        read_msg = i2c_msg.read(BH1750_ADDRESS, 2)
        bus.i2c_rdwr(read_msg)
        bytes_read = list(read_msg)
        return round(((bytes_read[0] << 8) + bytes_read[1]) / 1.2, 2)
    except Exception as e:
        print(f"Error reading light sensor: {e}")
        return None

def read_temp_sensor(bus):
    try:
        bus.write_byte_data(BMP280_ADDRESS, 0xF4, 0x27)
        time.sleep(0.1)
        raw_temp = bus.read_i2c_block_data(BMP280_ADDRESS, 0xFA, 3)
        raw_temp = ((raw_temp[0] << 12) | (raw_temp[1] << 4) | (raw_temp[2] >> 4))
        return round(raw_temp / 5120.0, 2)  # Simplified calculation
    except Exception as e:
        print(f"Error reading temperature sensor: {e}")
        return None

def publish_data(temp, light, goal_temp, goal_lux, brightness):
    payload = f"field1={temp}&field2={light}&field3={goal_temp}&field4={goal_lux}&field5={brightness}&status=MQTTPUBLISH"
    print("Publishing data:", payload)
    client.publish(MQTT_TOPIC, payload, qos=0)

def main():
    bus = SMBus(I2C_BUS)
    goal_temp = 22
    goal_lux = 100
    current_brightness = 50
    
    try:
        while True:
            temp = read_temp_sensor(bus)
            light = read_light_sensor(bus)
            publish_data(temp, light, goal_temp, goal_lux, current_brightness)
            time.sleep(15)
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        bus.close()
        wiringpi.digitalWrite(HEATER_RELAY_PIN, 1)
        wiringpi.softPwmWrite(LED_PIN, 0)
        print("Cleanup complete")

if __name__ == "__main__":
    main()
