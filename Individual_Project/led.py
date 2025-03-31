import time
import wiringpi

# Set the GPIO pin for the LED
pin = 3  # GPIO pin for the LED (change as necessary)

# Setup the wiringPi library
wiringpi.wiringPiSetup()  # Initializes wiringPi

# Set the pin as a PWM output
wiringpi.softPwmCreate(pin, 0, 100)  # Pin, initial PWM value, PWM range (0-100)

def control_led_brightness(brightness, wait_time):
    """
    Controls the LED brightness using PWM.
    
    :param brightness: The PWM duty cycle (0-100)
    :param wait_time: Time to wait between adjustments (in seconds)
    """
    # Set the PWM duty cycle for the LED
    wiringpi.softPwmWrite(pin, brightness)
    print(f"LED brightness set to {brightness}%")
    
    # Wait for a while to see the effect
    time.sleep(wait_time)

# Test the LED by gradually increasing brightness
for brightness in range(0, 101, 10):  # From 0 to 100, stepping by 10
    control_led_brightness(brightness, 1)  # Set brightness and wait for 1 second

# Cleanup when done
wiringpi.softPwmStop(pin)
print("PWM control stopped")
