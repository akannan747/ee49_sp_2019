from mqttclient import MQTTClient
from time import sleep
import math

server = "io.adafruit.com"
# update with your values from AdafruitIO ...
aio_user = "ashwin_kannan"
aio_key = "73609b18b6204c14aa793035fce4161d"

mqtt = MQTTClient(server=server, user=aio_user, password=aio_key, ssl=True)

for t in range(100):
    s = math.sin(t/10)
    mqtt.publish("{}/feeds/sms-feed".format(aio_user), str(s))
    time.sleep(3)