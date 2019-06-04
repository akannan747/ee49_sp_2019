from machine import Pin, PWM


class DRV8833:
    
    def __init__(self, pinA, pinB, frequency=10000):
        '''Instantiate controller for one motor.
        pinA: pin connected to AIN1 or BIN1
        pinB: pin connected to AIN2 or BIN2
        frequency: pwm frequency
        '''
        self.pin1 = PWM(Pin(pinA), freq=frequency)
        self.pin2 = PWM(Pin(pinB), freq=frequency)
        self.pin1.duty(100)
        self.pin2.duty(100)

    def set_speed(self, value):
        '''value: -100 ... 100 sets speed (duty cycle) and direction'''
        value = max(-100, min(100, value))
        if value > 0:
            self.pin1.duty(100)
            self.pin2.duty(100 - value)
        else:
            self.pin1.duty(100 + value)
            self.pin2.duty(100)
        #else:
        #    self.pin1.duty(value)
        #    self.pin2.duty(value) 