from machine import Pin, I2C, Timer
from board import *
from bno055 import BNO055 # IMU

from drv8833 import DRV8833 # your implementation
from motor import PIDMotor # your implementation, make sure this is named right!
from encoder import Encoder # your implementation, don't forget clear_count
from balance import Balance

import gc # for garbage collection methods

i2c = I2C(0, sda=23, scl=22, freq=12500)
imu = BNO055(i2c)

accel = imu.accelerometer()
alpha = 90 - math.asin(accel/9.8)
actual = imu.euler()

print(alpha)
print(actual)
