import Jetson.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
while True:
    print("High!")
    GPIO.output(7, GPIO.HIGH)
    time.sleep(1)
    print("Low!")
    GPIO.output(7, GPIO.LOW)
    time.sleep(1)
GPIO.cleanup()
