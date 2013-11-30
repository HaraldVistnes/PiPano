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

class DS18B20:
    def __init__(self):
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')  

        self.sensor_id_std = '28-000004619c93'   # standard sensor
        self.sensor_id_wp  = '28-0000049861cc'   # waterproof sensor
        self.base_dir = '/sys/bus/w1/devices/'

    def read_temp_raw(self, sensor_id):
        filename = self.base_dir + sensor_id + '/w1_slave'
        f = open(filename, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def read_temp(self, sensor_id):
        lines = self.read_temp_raw(sensor_id)
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_temp_raw(sensor_id)
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c
        else:
            return -1000.0 # something is wrong!

    def read_temps(self):
        return (self.read_temp(self.sensor_id_std), self.read_temp(self.sensor_id_wp))            

if __name__ == "__main__":
    # script
    GPIO.setmode(GPIO.BCM)
    ds18b20 = DS18B20()
    while True:
        print ds18b20.read_temps()
        time.sleep(1.0)

