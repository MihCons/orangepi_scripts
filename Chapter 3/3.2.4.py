import wiringpi as wp
import time

# Pin assignments
LED_PIN = 1  # LED on GPIO 1 (output)
SWITCH_PIN = 2  # Switch on GPIO 2 (input)

# Initialize wiringPi
wp.wiringPiSetup()

# Set LED pin as output
wp.pinMode(LED_PIN, wp.OUTPUT)

# Set switch pin as input
wp.pinMode(SWITCH_PIN, wp.INPUT)

# Enable internal pull-up resistor on GPIO 2 (for the switch)
wp.pullUpDnControl(SWITCH_PIN, wp.PUD_UP)

# Function to generate a short pulse (dot)
def short_pulse():
    wp.digitalWrite(LED_PIN, wp.HIGH)  # LED ON
    time.sleep(0.5)                    # Short pulse (0.5 seconds)
    wp.digitalWrite(LED_PIN, wp.LOW)   # LED OFF
    time.sleep(0.5)                    # Wait for 0.5 seconds before the next pulse

# Function to generate a long pulse (dash)
def long_pulse():
    wp.digitalWrite(LED_PIN, wp.HIGH)  # LED ON
    time.sleep(1.5)                    # Long pulse (1.5 seconds)
    wp.digitalWrite(LED_PIN, wp.LOW)   # LED OFF
    time.sleep(0.5)                    # Wait for 0.5 seconds before the next pulse

# Function to generate an SOS signal
def sos_signal():
    for _ in range(3):  # Repeat SOS three times
        # SOS in Morse code: ... --- ...
        for _ in range(3):  # Three short pulses for "..."
            short_pulse()
        for _ in range(3):  # Three long pulses for "---"
            long_pulse()
        for _ in range(3):  # Three short pulses for "..."
            short_pulse()

# Main loop
while True:
    if wp.digitalRead(SWITCH_PIN) == wp.LOW:  # Switch is pressed (active)
        print("SOS signal stopped.")
        wp.digitalWrite(LED_PIN, wp.LOW)  # Turn off LED if switch is pressed
        time.sleep(0.1)  # Small delay to avoid bouncing
    else:  # Switch is not pressed
        print("Sending SOS signal...")
        sos_signal()  # Generate SOS signal
