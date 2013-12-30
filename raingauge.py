#!/usr/bin/env python
""" Module for reading the temperature using a DS18B20 1-wire temperature sensor.

    Copyright (C) 2013 Harald Vistnes <harald.vistnes@gmail.com>

    This implementation is based on the tutorial
    http://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/

    NB! The DS18B20 temperature sensor MUST be connected to 
    GPIO #4 as that is the only pin that is supported by
    the 1-Wire protocol.
"""

import RPi.GPIO as GPIO, time, os, glob

channel = 22
counter = 0

def my_callback(channel):
    print 'Callback'

if __name__ == "__main__":
    # script
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(channel, GPIO.FALLING, callback=my_callback)

    while (True):
        if GPIO.input(channel):
            print 'HIGH'
        else:
            print 'LOW'
        time.sleep(0.5)

