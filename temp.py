#!/usr/bin/env python
""" Module for reading the temperature using a DS18B20 1-wire temperature sensor.

    Copyright (C) 2013 Harald Vistnes <harald.vistnes@gmail.com>

    This implementation is based on the tutorial
    http://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/

"""

import RPi.GPIO as GPIO, time, os, glob

class DS18B20:
    def __init__(self):
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')  

        self.base_dir = '/sys/bus/w1/devices/'
        self.device_folder = glob.glob(self.base_dir + '28*')[0]
        self.device_file = self.device_folder + '/w1_slave'

    def read_temp_raw(self):
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def read_temp():
        lines = read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c
        else:
            return -1000.0 # something is wrong!


if __name__ == "__main__":
    # script
    GPIO.setmode(GPIO.BCM)
    ds18b20 = DS18B20()
    while True:
        print ds18b20.read_temp()
        time.sleep(1.0)

