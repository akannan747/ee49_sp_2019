import paho.mqtt.client as paho
import matplotlib.pyplot as plt
import numpy as np

# Important: change the line below to a unique string,
# e.g. your name & make corresponding change in mqtt_plot_mpy.py
session = "rimuru"
BROKER = "iot.eclipse.org"
qos = 0

# connect to MQTT broker
print("Connecting to MQTT broker", BROKER, "...", end="")
mqtt = paho.Client()
mqtt.connect(BROKER, 1883)
print("Connected!")

# initialize data vectors
#cps_A = []
#cps_B = []
cps = []
t = []
#speeds = [-100, -90, -80, -70, -60, -50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
#time = np.arange(50)

# mqtt callbacks
def data1(c, u, message):
    # extract data from MQTT message
    msg = message.payload.decode('ascii')
    # convert to vector of floats
    f = [ float(x) for x in msg.split(',') ]
    print("received", f)
    # append to data vectors, add more as needed
    t.append(f[0])
    cps.append(f[1])

def data2(c, u, message):
    # extract data from MQTT message
    msg = message.payload.decode('ascii')
    # convert to vector of floats
    f = [ float(x) for x in msg.split(',') ]
    print("received", f)
    # append to data vectors, add more as needed
    t.append(f[0])
    cps.append(f[1])
    
def data3(c, u, message):
    # extract data from MQTT message
    msg = message.payload.decode('ascii')
    # convert to vector of floats
    f = [ float(x) for x in msg.split(',') ]
    print("received", f)
    # append to data vectors, add more as needed
    t.append(f[0])
    cps.append(f[1])

def data4(c, u, message):
    # extract data from MQTT message
    msg = message.payload.decode('ascii')
    # convert to vector of floats
    f = [ float(x) for x in msg.split(',') ]
    print("received", f)
    # append to data vectors, add more as needed
    t.append(f[0])
    cps.append(f[1])

def plot(client, userdata, message):
    # customize this to match your data
    print("plotting ...")
    plt.plot(t, cps,'.')
    #plt.plot(time, cps_B,'.')
    plt.xlabel("time")
    plt.ylabel("Left motor, right motor")
    plt.show()

# subscribe to topics
data_topic1 = "{}/data1".format(session, qos)
data_topic2 = "{}/data2".format(session, qos)
data_topic3 = "{}/data3".format(session, qos)
data_topic4 = "{}/data4".format(session, qos)
plot_topic = "{}/plot".format(session, qos)
mqtt.subscribe(data_topic1)
mqtt.subscribe(data_topic2)
mqtt.subscribe(data_topic3)
mqtt.subscribe(data_topic4)
mqtt.subscribe(plot_topic)
mqtt.message_callback_add(data_topic1, data1)
mqtt.message_callback_add(data_topic2, data2)
mqtt.message_callback_add(data_topic3, data3)
mqtt.message_callback_add(data_topic4, data4)
mqtt.message_callback_add(plot_topic, plot)

# wait for MQTT messages
# this function never returns
print("waiting for data ...")
mqtt.loop_forever()