from motor import *
from drv8833 import *
from encoder import *
from machine import Timer

desired_cps = 2750    # controller setpoint
P = 0.02              # controller proportional gain
Ts = 20               # controller operating period in [ms]

#controller = PIDMotor(DRV8833(19, 16), Encoder(34, 39, 0))
controller = PIDMotor(DRV8833(17, 21), Encoder(36, 4, 1))

def callback(timer):
    global controller, desired_cps, P
    # proportional control and print actual_cps (for plotting)
    print(controller.p_control(desired_cps, P))

timer = Timer(0)
timer.init(period=Ts, mode=Timer.PERIODIC, callback=callback(timer))