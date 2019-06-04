from time import sleep
from machine import deepsleep, Pin
from board import LED

led = Pin(LED, mode=Pin.OUT)     
led(1)                                             
sleep(10)                                       
led(0)                           
deepsleep(15000)  