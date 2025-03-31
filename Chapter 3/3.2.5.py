import time
import wiringpi

# GPIO pins for the LEDs (A, B, C, D)
led_pins = [1, 2, 5, 7]
# Pin for the switch (GPIO 2)
switch_pin = 2

# Set up wiringPi
wiringpi.wiringPiSetup()

# Set each pin as an output (LEDs)
for pin in led_pins:
    wiringpi.pinMode(pin, 1)

# Set the switch pin as an input
wiringpi.pinMode(switch_pin, 0)  # 0 is INPUT mode

# Function to run the light from left to right
def run_left_to_right():
    for pin in led_pins:
        wiringpi.digitalWrite(pin, 1)  # Turn LED on
        time.sleep(0.1)  # Wait for 0.1 seconds
        wiringpi.digitalWrite(pin, 0)  # Turn LED off

# Function to run the light from right to left
def run_right_to_left():
    for pin in reversed(led_pins):  # Reverse the order of the pins
        wiringpi.digitalWrite(pin, 1)  # Turn LED on
        time.sleep(0.1)  # Wait for 0.1 seconds
        wiringpi.digitalWrite(pin, 0)  # Turn LED off

# Running light effect
while True:
    # Check if the switch is pressed (activated = LOW)
    if wiringpi.digitalRead(switch_pin) == 0:  # Switch is pressed
        run_left_to_right()  # Move the light from left to right
    else:  # Switch is not pressed
        run_right_to_left()  # Move the light from right to left
