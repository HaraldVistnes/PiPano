#!/usr/bin/env python
""" Module for reading the temperature using a DS18B20 1-wire temperature sensor.

    Copyright (C) 2013 Harald Vistnes <harald.vistnes@gmail.com>

    This implementation is based on the tutorial
    http://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/

"""

import RPi.GPIO as GPIO, time, os, glob

# digital pin used by photocell
_defaultPin = 17

class DS18B20:
    def __init__(self, pin):
        self.pin = pin
        self.base_dir = '/sys/bus/w1/devices/'
        self.device_folder = glob.glob(self.base_dir + '28*')[0]
        self.device_file = self.device_folder + '/w1_slave'

        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')  

    def read_temp_raw(self):
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

if __name__ == "__main__":
    # script
    GPIO.setmode(GPIO.BCM)
    ds18b20 = DS18B20(_defaultPin)
    while True:
        print ds18b20.read_temp_raw()
        time.sleep(1.0)

