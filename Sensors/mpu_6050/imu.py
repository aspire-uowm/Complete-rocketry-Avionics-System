from mpu6050 import mpu6050

import time

sensor = mpu6050(0x68)

while (1):
	accelerometer_data = sensor.get_accel_data()

	print(accelerometer_data)
	time.sleep(1)
