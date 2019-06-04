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
            self.pin2.duty(100 - value)
        elif value < 0:
            self.pin1.duty(100 - (-1 * value))
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
        self.count = self.dec.count()
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

class MotorController:

    def __init__(self, motor, encoder):
        '''Controller for a single motor
        motor: motor driver (DRV8833)
        encoder: motor encoder (Encoder)
        '''
        self.mot = motor
        self.end = encoder
        self.integ = 0

    def p_control(self, desired_cps, P=1):
        '''Set motor control to rotate at desired_cps'''
        actual_cps = self.end.get_cps()
        error = desired_cps - actual_cps
        self.mot.set_speed(P*error)
        # return speed (e.g. for plotting)
        return actual_cps
    
    # add new method:
    def pi_control(self, desired_cps, Ts, P=1, I=1):
        actual_cps = self.end.get_cps()
        error = desired_cps - actual_cps
        self.integ += error * Ts/100
        # clamp integrator, e.g. if desired_cps exceeds maximum motor speed
        self.integ = max(-150, min(self.integ, 150))
        self.mot.set_speed(P*error + I*self.integ)
        return actual_cps
    
desired_cps = 2750    # controller setpoint
P = 0.02              # controller proportional gain
Ts = 20               # controller operating period in [ms]
I = 0.01

controller = MotorController(DRV8833(19, 16), Encoder(34, 39, 0))

def callback(timer):
    global controller, desired_cps, P
    # proportional control and print actual_cps (for plotting)
    print(controller.pi_control(desired_cps, P))

timer = Timer(0)
timer.init(period=Ts, mode=Timer.UP, callback=callback(timer))
