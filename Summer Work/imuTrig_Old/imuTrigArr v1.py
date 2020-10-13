from mpu6050 import mpu6050
import time

sensor = mpu6050(0x68)
gyro_list = []
accel_list = []
gyro_axis = 'x'
accel_axis = 'z'
delay = 0.1
sps = 1/delay #samples per second

while True:
	if len(gyro_list) >= 2*sps: #when the lists reach 2 seconds of data, delete the oldest samples
		gyro_list.pop(0)
		accel_list.pop(0)
	arm_raised = False
    gyroData = sensor.get_gyro_data()
    accelData = sensor.get_accel_data()
    gyro_list.append(gyroData[gyro_axis])
    accel_list.append(accelData[accel_axis])
    if gyroData[gyro_axis] > 120 and accelData[accel_axis] > 7: #first layer of threshold
    	minGyro_ind = gyro_list.index(min(gyro_list)) #get the index of the lower peak for gyro
    	minAccel_ind = accel_list.index(min(accel_list)) #get index of lower peak for accel from the last 2 seconds
    	if gyro_list[minGyro_ind] < 0 and accel_list[minAccel_ind] < 2 \
    	and (minGyro_ind, minAccel_ind) < (2*sps, 2*sps): #if arm is near pointing the ground prior to it being raised above the first threshold. 
    	#Also checks that the minimum's are before the high peak. 
    		arm_raised = True
    print("Arm raised: " + str(arm_raised))
    time.sleep(delay)
