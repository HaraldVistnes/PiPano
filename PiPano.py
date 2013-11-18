import RPi.GPIO as GPIO
import time
import os
import math

int halfSteps = 4

# motor speed
delay = 0.01

dir = "/mnt/usb/images"
if (not os.path.isdir(dir)):
	dir = "/home/pi/images"


GPIO.setmode(GPIO.BCM)

coilA1Pin = 24
coilA2Pin = 25
coilB1Pin = 23
coilB2Pin = 18

GPIO.setup(coilA1Pin, GPIO.OUT)
GPIO.setup(coilA2Pin, GPIO.OUT)
GPIO.setup(coilB1Pin, GPIO.OUT)
GPIO.setup(coilB2Pin, GPIO.OUT)

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
	os.system("raspistill -o " + dir + "/img_" + timestamp + "_" + arg + ".jpg" + opt)



try:

	# rotate camera range/2 counterclockwise

	print 'Turn 90 degrees CCW'
	backward(delay, halfSteps)
	time.sleep(0.5)

	for i in range(0, halfSteps*2+1):
		print 'Step ' + str(i)
		capture(str(i+1))
		forward(delay, 1)	
		time.sleep(0.5)

	print 'Turn back to start position'
	backward(delay, halfSteps)

finally:
	release()
	GPIO.cleanup()

#for img in os.listdir(dir):
#       filename = dir + "/" + img
#       os.system("dropbox_uploader.sh upload " + filename)
#       os.remove(filename)


