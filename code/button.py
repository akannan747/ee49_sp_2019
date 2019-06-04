from machine import Pin
from time import sleep
#from board import A20
#from micropython import schedule

def report(pin):
    pin(1)
    sleep(0.01)
    pin.init(mode=Pin.IN)
    for i in range(300):
        # check if d is zero
        if pin() == 0:
            print("count", i)
            break

while True:
    button = Pin(17, mode=Pin.OUT) 
    report(button)
    sleep(0.01)
