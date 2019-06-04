from mqttclient import MQTTClient
import network
import math
from ina219 import INA219
from machine import I2C, Pin
from board import SDA, SCL
import time

i2c = I2C(id=0, scl=Pin(SCL), sda=Pin(SDA), freq = 100000)
SHUNT_RESISTOR_OHMS = 0.1
ina = INA219(SHUNT_RESISTOR_OHMS, i2c)
ina.configure()

def solar():
    v = ina.voltage()
    i = ina.current()
    p = ina.power()
    r = v/i
    print("V = {:6.2f}, I = {:6.2f}, P = {:6.2f}, R = {:6.2f}".format(v, i, p, r))
    time.sleep(0.5)
    
    return v, i, p, r

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
r = 0
while r < 1:
    v, i, p, r = solar()
    # add additional values as required by application
    topic = "{}/data".format(session)
    data = "{},{},{},{}".format(v, i, p, r)
    print("send topic='{}' data='{}'".format(topic, data))
    mqtt.publish(topic, data)

# do the plotting (on host)
print("tell host to do the plotting ...")
mqtt.publish("{}/plot".format(session), "create the plot")

# free up resources
# alternatively reset the microphyton board before executing this program again
mqtt.disconnect()