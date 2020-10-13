from mpu6050 import mpu6050
import time

sensor = mpu6050(0x68)
while True:
	arm_raised = False
    gyroData = sensor.get_gyro_data()
    accelData = sensor.get_accel_data()
    if gyroData['x'] > 100 and accelData['z'] > 5:
    	arm_raised = True
    print("Arm raised: " + str(arm_raised)
    time.sleep(0.2)
