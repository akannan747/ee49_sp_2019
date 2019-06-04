from board import ADC0, A21, A20
from machine import Pin, ADC
from micropython import const
import time

DEBOUNCE_MS = const(50)
offset = 0
gram_factor = 2
ounce_factor = 0.071
factor = gram_factor

adc0 = ADC(Pin(ADC0))
# set full-scale range
adc0.atten(ADC.ATTN_6DB)

def callback():
    global offset
    offset = adc0.read()

def switch_units():
    global factor
    if factor == gram_factor:
        factor = ounce_factor
    else:
        factor = gram_factor

button = Pin(A21, mode=Pin.IN, pull=Pin.PULL_UP)
button2 = Pin(A20, mode=Pin.IN, pull=Pin.PULL_UP)

last_time_ms = 0    # stores last time a change was detected
last_time_ms2 = 0
last_state = button()
last_state2 = button2()

while True:
    d_out = adc0.read()
    output = (d_out - offset) * factor
    button_state = button()
    button_state2 = button2()
    if button_state != last_state:
        # detected a change
        t = time.ticks_ms()   # current time in ms
        if abs(t - last_time_ms) > DEBOUNCE_MS:
            # change detected, take action (e.g. advance counter)
            callback()
            last_time_ms = t
            last_state = button_state
    if button_state2 != last_state2:
        # detected a change
        t = time.ticks_ms()   # current time in ms
        if abs(t - last_time_ms2) > DEBOUNCE_MS:
            # change detected, take action (e.g. advance counter)
            switch_units()
            last_time_ms2 = t
            last_state2 = button_state2
    
    print(output)
    time.sleep(1)