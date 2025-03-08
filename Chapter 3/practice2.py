import time
import wiringpi

led_pins = [1, 2, 5, 7] 

wiringpi.wiringPiSetup()


for pin in led_pins:
    wiringpi.pinMode(pin, 1)


while True:
    
    for pin in led_pins:
        wiringpi.digitalWrite(pin, 1)
    time.sleep(0.1) 

    for pin in led_pins:
        wiringpi.digitalWrite(pin, 0)
    time.sleep(0.1) 