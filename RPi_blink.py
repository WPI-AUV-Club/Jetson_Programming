#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

# Pin Definitons:
led_pin = 12  # BOARD pin 12
# but_pin = 18  # BOARD pin 18

def main():
    prev_value = None

    # Pin Setup:
    GPIO.setmode(GPIO.BOARD)  # BOARD pin-numbering scheme
    GPIO.setup(led_pin, GPIO.OUT)  # LED pin set as output
    # GPIO.setup(but_pin, GPIO.IN)  # Button pin set as input

    # Initial state for LEDs:
    curr_value = GPIO.HIGH
    GPIO.output(led_pin, curr_value)
    try:
        while True:
            curr_value = not curr_value
            GPIO.output(led_pin, not curr_value)
            print("Outputting {} to Pin {}".format(curr_value, led_pin))
            time.sleep(1)
    finally:
        GPIO.cleanup()  # cleanup all GPIO

if __name__ == '__main__':
    main()
