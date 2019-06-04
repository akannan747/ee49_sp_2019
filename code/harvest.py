from busio import I2C
from board import SDA, SCL
from adafruit_bme680 import Adafruit_BME680_I2C as BME680

i2c = I2C(scl=SCL, sda=SDA)
bme = BME680(i2c, address=0x76)

temperature = []
gas = []
humidity = []
pressure = []
altitude = []

#while True:
for i in range(10):
    print(bme.temperature, bme.gas, bme.humidity, bme.pressure, bme.altitude)
    #temperature += [bme.temperature]
    #gas += [bme.gas]
    #humidity += [bme.humidity]
    #pressure += [bme.pressure]
    #altitude += [bme.altitude]
    #time.sleep(1)
    
