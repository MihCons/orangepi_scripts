import time
import wiringpi

# GPIO pins for the LEDs (A, B, C, D)
led_pins = [1, 2, 5, 7]

# Set up wiringPi
wiringpi.wiringPiSetup()

# Set each pin as an output
for pin in led_pins:
    wiringpi.pinMode(pin, 1)

# Running light effect with specified timing
while True:
    # Turn LED1 and LED3 on and off together
    wiringpi.digitalWrite(led_pins[0], 1)  # Turn LED1 on
    wiringpi.digitalWrite(led_pins[2], 1)  # Turn LED3 on
    time.sleep(0.5)  # Wait for 0.5 seconds
    wiringpi.digitalWrite(led_pins[0], 0)  # Turn LED1 off
    wiringpi.digitalWrite(led_pins[2], 0)  # Turn LED3 off
    time.sleep(0.5)  # Wait for 0.5 seconds

    # Turn LED2 and LED4 on and off together with a 1-second interval
    wiringpi.digitalWrite(led_pins[1], 1)  # Turn LED2 on
    wiringpi.digitalWrite(led_pins[3], 1)  # Turn LED4 on
    time.sleep(0.5)  # Wait for 0.5 seconds
    wiringpi.digitalWrite(led_pins[1], 0)  # Turn LED2 off
    wiringpi.digitalWrite(led_pins[3], 0)  # Turn LED4 off
    time.sleep(1)  # Wait for 1 second
