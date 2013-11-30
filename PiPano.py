#!/usr/bin/env python

""" Script for capturing a panorama scene using a stepper motor
    to rotate the Raspberry PI Camera module

    Copyright (C) 2013 Harald Vistnes <harald.vistnes@gmail.com>

"""

import RPi.GPIO as GPIO
import time
import os
import math
import photocell

halfSteps = 3

# motor speed
delay = 0.01

dir_images = "/mnt/usb/images"
dir_sensors = "/mnt/usb/sensors"

# mount the USB stick if it is not found
if (not os.path.isdir(dir_images)):
    os.system("mount -t vfat /dev/sda1 /mnt/usb/")

# if still no success, the USB stick is probably removed,
# use a folder on the memory card
if (not os.path.isdir(dir_images)):
    dir_images = "/home/pi/images"
    dir_sensors = "/home/pi/sensors"

GPIO.setmode(GPIO.BCM)

coilA1Pin = 24
coilA2Pin = 25
coilB1Pin = 23
coilB2Pin = 18

GPIO.setup(coilA1Pin, GPIO.OUT)
GPIO.setup(coilA2Pin, GPIO.OUT)
GPIO.setup(coilB1Pin, GPIO.OUT)
GPIO.setup(coilB2Pin, GPIO.OUT)

# instantiate photocell
pc = photocell.PhotoCell()

now = time.localtime(time.time())
timestamp = time.strftime("%Y%m%d_%H%M", now)
opt = " -w 2592 -h 1944 -hf -vf -n -q 100 -t 2000 -sh 0 -ISO 100 -awb horizon"

def setStep(w1, w2, w3, w4):     
    GPIO.output(coilA1Pin, w1) 
    GPIO.output(coilA2Pin, w2)
    GPIO.output(coilB1Pin, w3) 
    GPIO.output(coilB2Pin, w4)

def forward(delay, steps):
    for i in range(0, steps):
        setStep(1, 0, 1, 0)
        time.sleep(delay)
        setStep(0, 1, 1, 0)
        time.sleep(delay)
        setStep(0, 1, 0, 1)
        time.sleep(delay)
        setStep(1, 0, 0, 1)
        time.sleep(delay)

def backward(delay, steps):
    for i in range(0, steps):
        setStep(1, 0, 0, 1)
        time.sleep(delay)
        setStep(0, 1, 0, 1)
        time.sleep(delay)
        setStep(0, 1, 1, 0)
        time.sleep(delay)
        setStep(1, 0, 1, 0)
        time.sleep(delay)

def release():
    setStep(0, 0, 0, 0)

def capture(arg):
    localdir = dir_images + "/" + arg
    if not os.path.exists(localdir):
        os.makedirs(localdir)
    os.system("raspistill -o " + localdir + "/img_" + timestamp + "_" + arg + ".jpg" + opt)

def read_photocell():
    rctime = pc.RCtime()
    if not os.path.exists(dir_sensors):
        os.makedirs(dir_sensors)
    filename = dir_sensors + "/photocell_" + time.strftime("%Y%m%d", now)
    with open(filename, 'a') as pcfile:
        pcfile.write(time.strftime("%H%M", now) + ', ' + str(rctime) + '\n')

try:
    # read light from photocell
    print 'Read photocell'
    read_photocell()

    # rotate camera range/2 counterclockwise

    print 'Turn 90 degrees CCW'
    backward(delay, halfSteps)
    time.sleep(0.5)

    for i in range(0, halfSteps*2):
        print 'Step ' + str(i)
        capture(str(i+1))
        forward(delay, 1)	
        time.sleep(0.5)

    capture(str(halfSteps*2+1))
    print 'Turn back to start position'
    backward(delay, halfSteps)

finally:
    release()
    GPIO.cleanup()

#for img in os.listdir(dir):
#       filename = dir + "/" + img
#       os.system("dropbox_uploader.sh upload " + filename)
#       os.remove(filename)


