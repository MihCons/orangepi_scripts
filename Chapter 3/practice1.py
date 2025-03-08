# Create an infinitely long flashing light. Use an LED connected to GPIO (eg. wiringpi pin w2).


import time
import wiringpi
import sys

def blink(pin):
    wiringpi.digitalWrite(pin, 1)
    time.sleep(0.5)
    wiringpi.digitalWrite(pin, 0)
    time.sleep(0.5)

# SETUP
print("Start")
pin = 2
wiringpi.wiringPiSetup()
wiringpi.pinMode(pin, 1) 

# MAIN
while True:
    blink(pin)

# cleanup
print("Done")
