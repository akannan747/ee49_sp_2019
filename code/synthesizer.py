# imports
from machine import Pin, PWM
from board import A0, A1
from time import sleep

# initialize PWM objects for all synthesizer inputs

pwm_filtered = PWM(Pin(25))    # PWM waveform A0 that passes through the filter
pwm_1 = PWM(Pin(13))          # PWM waveform D4 passed to amplifier without filtering

def play(pwmout, enable=False, freq=100):
    '''if enable, generate pwm signal on pwmout with specified frequency
           otherwise set the pwm output to 0.'''
    # Hint: adjust the duty cycle to achieve this functionality
    if enable:
        pwmout.freq(freq)
        pwmout.duty(50)
    else:
        pwmout.duty(0)

# enable the amplifier ...

# alternatively play the filtered and unfiltered output
freq = 100
filtered = True
while True:
    play(pwm_filtered, enable=filtered, freq=freq)
    play(pwm_1, enable=not filtered, freq=freq)
    print("playing, filtered", filtered)
    sleep(2)
    filtered = not filtered
    freq += 100
    
    