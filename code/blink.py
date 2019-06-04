from machine import Pin
from board import LED
import time

led = Pin(LED, mode=Pin.OUT)

while True:
    led(1)
    time.sleep(.666)
    led(0)
    time.sleep(.666)