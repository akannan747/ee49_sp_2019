from machine import Pin, DEC, PWM
import time

class DRV8833:
    
    def __init__(self, pinA, pinB, frequency=10000):
        '''Instantiate controller for one motor.
        pinA: pin connected to AIN1 or BIN1
        pinB: pin connected to AIN2 or BIN2
        frequency: pwm frequency
        '''
        self.pin1 = PWM(Pin(pinA), freq=frequency, timer=2)
        self.pin2 = PWM(Pin(pinB), freq=frequency, timer=3)

    def set_speed(self, value):
        '''value: -100 ... 100 sets speed (duty cycle) and direction'''
        if value > 0:
            self.pin1.duty(100)
            self.pin2.duty(value)
        elif value < 0:
            self.pin1.duty(value)
            self.pin2.duty(100)
        else:
            self.pin1.duty(value)
            self.pin2.duty(value) 
            
class Encoder:

    def __init__(self, chA, chB, unit, counts_per_turn=24*75, wheel_diameter=330):
        '''Decode output from quadrature encoder connected to pins chA, chB.
        unit: DEC unit to use (0 ... 7).
        counts_per_turn: Number of counts per turn of the motor drive shaft. For scaling cps to rpm.
        wheel_diameter: In [mm]. For scaling count to distance traveled.
        '''
        self.p1 = Pin(chA, mode=Pin.IN)
        self.p2 = Pin(chB, mode=Pin.IN)
        self.cpt = counts_per_turn
        self.dia = wheel_diameter
        self.dec = DEC(unit, self.p1, self.p2)
        self.count = 0
        self.time = time.time()
        self.cps = 0

    def get_count(self):           
        return self.dec.count()

    def get_distance(self):        
        return get_count() / self.cpt * 3.14 * self.dia / 1000

    def get_cps(self):             
        count = self.dec.count()
        curr_time = time.time()
        diff = count - self.count
        timediff = curr_time - self.time
        self.time = curr_time
        self.count = self.dec.count()
        self.cps = diff/timediff
        return self.cps

    def get_rpm(self):             
        return self.get_cps()/self.cpt * 60
        
        
motorA = DRV8833(19, 16)     
motorB = DRV8833(17, 21)  

encA = Encoder(34, 39, 0)          
encB = Encoder(36,  4, 1) 


while True:
    value = encA.get_cps()
    print(value)
    time.sleep(1)
