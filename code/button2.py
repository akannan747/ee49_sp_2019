from machine import Pin
from time import sleep
from board import LED
#from micropython import schedule

led = Pin(LED, mode=Pin.OUT)

def on(pin):
    pin(1)
    sleep(0.01)
    pin.init(mode=Pin.IN)
    for i in range(300):
        # check if d is zero
        if pin() == 0:
            if i > 10:
                led(1)
            break
            
def off(pin):
    pin(1)
    sleep(0.01)
    pin.init(mode=Pin.IN)
    for i in range(300):
        # check if d is zero
        if pin() == 0:
            if i > 10:
                led(0)
            break
            
def flash(pin):
    pin(1)
    sleep(0.01)
    pin.init(mode=Pin.IN)
    for i in range(300):
        # check if d is zero
        if pin() == 0:
            if i > 10:
                led(1)
                sleep(1)
                led(0)
                led(1)
                sleep(1)
                led(0)
            break
            
while True:
    button4 = Pin(17, mode=Pin.OUT)
    button3 = Pin(16, mode=Pin.OUT)
    button2 = Pin(19, mode=Pin.OUT)
    on(button4)
    off(button3)
    flash(button2)
    sleep(0.01)
