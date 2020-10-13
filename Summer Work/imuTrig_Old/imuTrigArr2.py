from mpu6050 import mpu6050
import time


sensor = mpu6050(0x68)
flag_list = []
gyro_axis = 'x'
accel_axis = 'z'
delay = 0.1
sps = int(1/delay) #samples per second

def check_last_sec(list_of_flag):
    i = 0
    num_consecutive = 0
    list_len = len(list_of_flag)
    while i < list_len:
        if list_of_flag[i] == True:
            num_consecutive += 1
        elif list_of_flag[i] == False and num_consecutive != 0: #this is to make sure that when we register Trues but then get a False, we break
            break
        i += 1
    if num_consecutive >= int(sps/2) - 1: #if half a second of data is shown to be true, then you can give the true flag. 
        return True
    return False

while True:
    if len(flag_list) > sps + 2: #keep size of flag list to a little more than 1 second of samples.
        flag_list.pop(0)
	t_flag = False
    arm_raised = False
    gyroData = sensor.get_gyro_data()
    accelData = sensor.get_accel_data()
    if gyroData[gyro_axis] > 120 and accelData[accel_axis] > 7: #first layer of threshold
    	t_flag = True
    elif gyroData[gyro_axis] < 80 and gyroData[gyro_axis] > 40 and accelData[accel_axis] > 7: #second layer
        t_flag = True
    elif gyroData[gyro_axis] < 30 and accelData[accel_axis] > 7: #third layer
        t_flag = True
    flag_list.append(t_flag)
    if flag_list[len(flag_list) - 1] == True and len(flag_list) >= sps:
        if check_last_sec(flag_list[int(sps/2):]): #sending half a second of data over
            arm_raised = True
    print("Arm raised: " + str(arm_raised))
    time.sleep(delay)
