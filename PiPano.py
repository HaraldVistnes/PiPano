import RPi.GPIO as GPIO
import time
import os

dir = "images"

GPIO.setmode(GPIO.BCM)

coilA1Pin = 4
coilA2Pin = 17
coilB1Pin = 23
coilB2Pin = 24

GPIO.setup(coilA1Pin, GPIO.OUT)
GPIO.setup(coilA2Pin, GPIO.OUT)
GPIO.setup(coilB1Pin, GPIO.OUT)
GPIO.setup(coilB2Pin, GPIO.OUT)

now = time.localtime(time.time())
timestamp = time.strftime("%Y%m%d_%H%M", now)
opt = " -w 2592 -h 1944 -hf -vf -n -q 100 -t 2000 -sh 0 -ISO 100 -awb horizon"

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

def setStep(w1, w2, w3, w4):     
        GPIO.output(coilA1Pin, w1) 
        GPIO.output(coilA2Pin, w2)
        GPIO.output(coilB1Pin, w3) 
        GPIO.output(coilB2Pin, w4)

def release():
        setStep(0, 0, 0, 0)

delay = 0.01
steps = 1
#os.system("raspistill -o images/img_" + timestamp + "_1.jpg" + opt)
print 'forward'
forward(delay, steps)
time.sleep(1.0)

#os.system("raspistill -o images/img_" + timestamp + "_2.jpg" + opt)
print 'forward'
forward(delay, steps)
time.sleep(1.0)
#os.system("raspistill -o images/img_" + timestamp + "_3.jpg" + opt)
print 'forward'
forward(delay, steps)
time.sleep(1.0)
#os.system("raspistill -o images/img_" + timestamp + "_4.jpg" + opt)
print 'backward'
backward(delay, 3*steps)

release()

GPIO.cleanup()

#for img in os.listdir(dir):
#       filename = dir + "/" + img
#       os.system("dropbox_uploader.sh upload " + filename)
#       os.remove(filename)


