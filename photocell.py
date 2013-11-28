#!/usr/bin/env python
""" Module for reading values from a photocell 

    This implementation is based on the tutorial
    http://learn.adafruit.com/basic-resistor-sensor-reading-on-raspberry-pi/basic-photocell-reading

    Uses RC (resistor-capacitor) circuit for reading the photocell
    value as the Raspberry PI does not have any analog pins.

    As the photocell behaves as a resistor that changes resistance
    based on the amount of incoming light, the time to charge 
    the capacitor will depend on the amount of light.

    The function RCtime returns the number of loops required to 
    charge the capacitor enough for the input pin to go from 
    low to high.

    The more light, the lower the resistance and the lower number
    returned from RCtime.

    RCtime - low value means more light than a higher value

    Copyright (C) 2013 Harald Vistnes <harald.vistnes@gmail.com>
"""

import RPi.GPIO as GPIO, time, os 

# digital pin used by photocell
_defaultPin = 4

class PhotoCell:
    def __init__(self, pin):
        self.pin = pin
	
    # returns a pseudo-timing of the time required for the pin
    # to get from low to high
    def RCtime(self):
        reading = 0
        
        # set the pin to low
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)
        time.sleep(0.1)

        # read from pin
        GPIO.setup(self.pin, GPIO.IN)
        # count the number of iterations required for the
        # pin to get high
        while (GPIO.input(self.pin) == GPIO.LOW):
            reading += 1
        return reading     

if __name__ == "__main__":
    # script
    GPIO.setmode(GPIO.BCM)
    pc = PhotoCell(_defaultPin)  
    while True:
        print pc.RCtime()
    GPIO.cleanup()

