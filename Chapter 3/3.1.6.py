import time
import wiringpi

# GPIO pin for SOS signal
sos_pin = 1

# Set up wiringPi
wiringpi.wiringPiSetup()

# Set pin as an output
wiringpi.pinMode(sos_pin, 1)

# SOS signal (continuous)
while True:
    # Short pulse
    wiringpi.digitalWrite(sos_pin, 1)  # Turn on
    time.sleep(0.5)  # Short pulse duration
    wiringpi.digitalWrite(sos_pin, 0)  # Turn off
    time.sleep(0.5)  # Short pause before next signal

    # Long pulse
    wiringpi.digitalWrite(sos_pin, 1)  # Turn on
    time.sleep(1.5)  # Long pulse duration
    wiringpi.digitalWrite(sos_pin, 0)  # Turn off
    time.sleep(0.5)  # Short pause before next signal

    # Short pulse again
    wiringpi.digitalWrite(sos_pin, 1)  # Turn on
    time.sleep(0.5)  # Short pulse duration
    wiringpi.digitalWrite(sos_pin, 0)  # Turn off
    time.sleep(1.5)  # Pause before repeating the pattern
