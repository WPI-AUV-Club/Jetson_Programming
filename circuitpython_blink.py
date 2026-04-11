import time
import board
import digitalio

print("hello blinky!")

led = digitalio.DigitalInOut(board.D18)
led.direction = digitalio.Direction.OUTPUT

while True:
    led.value = True
    print("high")
    time.sleep(0.5)
    led.value = False
    print("low")
    time.sleep(0.5)
