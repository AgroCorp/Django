import RPi.GPIO as GPIO
from time import sleep

RED = 37
GREEN = 40
YELLOW = 38

def led_blink(time, pin):
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

	GPIO.output(pin, GPIO.HIGH)
	sleep(time)
	GPIO.output(pin, GPIO.LOW)
