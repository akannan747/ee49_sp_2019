from mqttclient import MQTTClient
from time import sleep
from machine import deepsleep
import math
from busio import I2C
from board import SDA, SCL
from adafruit_bme680 import Adafruit_BME680_I2C as BME680

i2c = I2C(scl=SCL, sda=SDA)
bme = BME680(i2c, address=0x76)

server = "io.adafruit.com"
# update with your values from AdafruitIO ...
aio_user = "ashwin_kannan"
aio_key = "dd9efcf7eb024bad8d4bf6cd16962973"

mqtt = MQTTClient(server=server, user=aio_user, password=aio_key, ssl=True)

while True:
    t = bme.temperature
    g = bme.gas
    h= bme.humidity
    p = bme.pressure
    a = bme.altitude
    mqtt.publish("{}/feeds/temperature".format(aio_user), str(t))
    mqtt.publish("{}/feeds/gas".format(aio_user), str(g))
    mqtt.publish("{}/feeds/humidity".format(aio_user), str(h))
    mqtt.publish("{}/feeds/pressure".format(aio_user), str(p))
    mqtt.publish("{}/feeds/altitude".format(aio_user), str(a))
    sleep(10)
    deepsleep(30000)  
    