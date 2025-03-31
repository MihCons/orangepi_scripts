import wiringpi as wp
import time

# Pin assignments
LED_PIN = 1  # LED on GPIO 1
SWITCH_PIN = 2  # Switch on GPIO 2
RELAY_PIN = 3  # Relay 1 control on GPIO 3 (IN1)

# Initialize wiringPi
wp.wiringPiSetup()

# Set LED pin as output
wp.pinMode(LED_PIN, wp.OUTPUT)

# Set switch pin as input
wp.pinMode(SWITCH_PIN, wp.INPUT)

# Set relay pin as output
wp.pinMode(RELAY_PIN, wp.OUTPUT)

# Enable internal pull-up resistor on GPIO 2 (for the switch)
wp.pullUpDnControl(SWITCH_PIN, wp.PUD_UP)

def blink_led():
    # Function to blink the LED
    wp.digitalWrite(LED_PIN, wp.HIGH)  # LED ON
    time.sleep(0.5)                    # Wait for 0.5 seconds
    wp.digitalWrite(LED_PIN, wp.LOW)   # LED OFF
    time.sleep(0.5)                    # Wait for 0.5 seconds

# Main loop
while True:
    # Check if the switch is pressed (closed)
    if wp.digitalRead(SWITCH_PIN) == wp.LOW:  # Switch is closed
        print("LED blinks")
        blink_led()  # Keep blinking the LED
        wp.digitalWrite(RELAY_PIN, wp.HIGH)  # Activate the relay (IN1)
    else:  # Switch is open
        print("LED not flashing")
        wp.digitalWrite(LED_PIN, wp.LOW)  # Ensure LED is turned off
        wp.digitalWrite(RELAY_PIN, wp.LOW)  # Deactivate the relay (IN1)
        time.sleep(0.1)  # Small delay to avoid bouncing issues
