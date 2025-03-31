import time
import wiringpi

# GPIO pins for the LEDs (A, B, C, D)
led_pins = [1, 2, 5, 7]

# Set up wiringPi
wiringpi.wiringPiSetup()

# Set each pin as an output
for pin in led_pins:
    wiringpi.pinMode(pin, 1)

# Running light effect
while True:
    for pin in led_pins:
        wiringpi.digitalWrite(pin, 1)  # Turn LED on
        time.sleep(0.1)  # Wait for 0.1 seconds
        wiringpi.digitalWrite(pin, 0)  # Turn LED off
