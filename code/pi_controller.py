from motor import *
from drv8833 import *
from encoder import *
from machine import Timer

desired_cps = 2750    # controller setpoint
P = 0.045              # controller proportional gain
Ts = 20               # controller operating period in [ms]
I = 0.5

controller = PIDMotor(DRV8833(19, 16), Encoder(39, 36, 1))
#controller = PIDMotor(DRV8833(17, 21), Encoder(36, 4, 1))

def callback(timer):
    global controller, desired_cps, P
    # proportional control and print actual_cps (for plotting)
    print(controller.pi_control(desired_cps, Ts, P, I))

timer = Timer(0)
timer.init(period=Ts, mode=Timer.PERIODIC, callback=callback)