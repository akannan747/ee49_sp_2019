from drv8833 import DRV8833
from encoder import Encoder

class PIDMotor:

    def __init__(self, motor, encoder):
        '''Controller for a single motor
        motor: motor driver (DRV8833)
        encoder: motor encoder (Encoder)
        '''
        self.mot = motor
        self.enc = encoder
        self.integ = 0

    def p_control(self, desired_cps, P=1):
        '''Set motor control to rotate at desired_cps'''
        actual_cps = self.enc.get_cps()
        error = desired_cps - actual_cps
        self.mot.set_speed(P*error)
        # return speed (e.g. for plotting)
        return actual_cps
    
    def pi_control(self, desired_cps, Ts, P=1, I=1):
        actual_cps = self.enc.get_cps()
        error = desired_cps - actual_cps
        self.integ += error * Ts/1000
        # clamp integrator, e.g. if desired_cps exceeds maximum motor speed
        self.integ = max(-150, min(self.integ, 150))
        self.mot.set_speed(P*error + I*self.integ)
        return actual_cps