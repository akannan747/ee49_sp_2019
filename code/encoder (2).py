from mqttclient import MQTTClient
import network
from machine import Pin
from machine import DEC
from DRV8833 import *
import time

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
        self.dec = DEC(unit, p1, p2)
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
        self.count = dec.count()
        self.cps = diff/timediff
        return self.cps

    def get_rpm(self):             
        return self.get_cps()/self.cpt * 60

def hot_wheels(speed):
    motorA = DRV8833(19, 16)     
    motorB = DRV8833(17, 21)  

    encA = Encoder(34, 39, 0)          
    encB = Encoder(36,  4, 1)   
    
    cps_A = None
    cps_B = None
    
    motorA.set_speed(speed)
    cps_A = encA.get_cps()
    motorA.set_speed(0)
    
    motorB.set_speed(speed)
    cps_B = encB.get_cps()
    motorB.set_speed(0)
    
    return cps_A, cps_B 

speeds = [-100, -90, -80, -70, -60, -50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

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

# send data
# In this sample, we send "fake" data. Replace this code to send useful data,
# e.g. measurement results.
for speed in speeds:
    cps_A, cps_B = hot_wheels(speed)
    # add additional values as required by application
    topic = "{}/data".format(session)
    data = "{},{}".format(cps_A, cps_B)
    print("send topic='{}' data='{}'".format(topic, data))
    mqtt.publish(topic, data)

# do the plotting (on host)
print("tell host to do the plotting ...")
mqtt.publish("{}/plot".format(session), "create the plot")

# free up resources
# alternatively reset the microphyton board before executing this program again
mqtt.disconnect()