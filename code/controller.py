from mqttclient import MQTTClient
import network
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

"""
def hot_wheels(speed):
    cps_A = []
    cps_B = []
    
    motorA.set_speed(speed)
    motorB.set_speed(speed)
    time.sleep(0.1)
    for i in range(100):
        cps_A.append(encA.get_cps())
        cps_B.append(encB.get_cps())
    motorA.set_speed(0)
    motorB.set_speed(0)
    return sum(cps_A)/len(cps_A), sum(cps_B)/len(cps_B) 


#speeds = [-100, -90, -80, -70, -60, -50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
speed = 50
"""

desired_cps = 2750    # controller setpoint
P = 0.02              # controller proportional gain
Ts = 20               # controller operating period in [ms]

# Initialize the motors and encoders.
motorA = DRV8833(19, 16)     
motorB = DRV8833(17, 21)  

encB = Encoder(34, 39, 0)          
encA = Encoder(36,  4, 1) 

controller = MotorController(motorA, encA)

# Important: change the line below to a unique string.
session = "rimuru"
BROKER = "iot.eclipse.org"

# check wifi connection
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
ip = wlan.ifconfig()[0]
if ip == '0.0.0.0':
    print("no wifi connection")
    # code to handle the problem ...
else:
    print("connected to WiFi at IP", ip)

# connect to MQTT broker
print("Connecting to MQTT broker", BROKER, "...", end="")
mqtt = MQTTClient(BROKER)
print("Connected!")

#for speed in speeds:
"""
for i in range(50):
    cps_A, cps_B = hot_wheels(speed)
    # add additional values as required by application
    topic = "{}/data".format(session)
    data = "{},{}".format(cps_A, cps_B)
    print("send topic='{}' data='{}'".format(topic, data))
    mqtt.publish(topic, data)
"""
t = 0
def callback():
    global controller, desired_cps, P, t
    # proportional control and print actual_cps (for plotting)
    cps = controller.p_control(desired_cps, P)
    t += Ts
    topic = "{}/data".format(session)
    data = "{},{}".format(t, cps)
    print("send topic='{}' data='{}'".format(topic, data))
    mqtt.publish(topic, data)

        
# do the plotting (on host)
print("tell host to do the plotting ...")
mqtt.publish("{}/plot".format(session), "create the plot")
# free up resources
# alternatively reset the microphyton board before executing this program again
mqtt.disconnect()
    


