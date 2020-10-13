from mpu6050 import mpu6050
import time


sensor = mpu6050(0x68)
flag_list = []
gyro_axis = 'x'
accel_axis = 'z'
delay = 0.1
sps = int(1/delay) #samples per second

def is_sublist(list1, sublist):
    sub_set = False
    if sublist == []:
        sub_set = True
    elif sublist == list1:
        sub_set = True
    elif len(sublist) > len(list1):
        sub_set = False
    else:
        for i in range(len(list1)):
            if list1[i] == sublist[0]:
                n = 1
                while (n < len(sublist)) and (list1[i+n] == sublist[n]):
                    n += 1
                if n == len(sublist):
                    sub_set = True
    return sub_set

def check_last_sec(list_of_flag):
    i = 0
    ideal_list = [1, 2, 3, 3, 3, 3]
    list_len = len(list_of_flag)
    if is_sublist(list_of_flag, ideal_list):
        return True
    return False

while True:
    if len(flag_list) > sps + 2: #keep size of flag list to a little more than 1 second of samples.
        flag_list.pop(0)
	flag1, flag2, flag3 = 1, 2, 3
    arm_raised = False
    gyroData = sensor.get_gyro_data()
    accelData = sensor.get_accel_data()
    if gyroData[gyro_axis] > 120 and accelData[accel_axis] > 7: #first layer of threshold
        flag_list.append(flag1)
    elif gyroData[gyro_axis] < 80 and gyroData[gyro_axis] > 40 and accelData[accel_axis] > 7: #second layer
        flag_list.append(flag2)
    elif gyroData[gyro_axis] < 30 and accelData[accel_axis] > 7: #third layer
        flag_list.append(flag3)
    if flag_list[len(flag_list) - 1] == True and len(flag_list) >= sps:
        if check_last_sec(flag_list[int(sps/2):]): #sending half a second of data over
            arm_raised = True
    print("Arm raised: " + str(arm_raised))
    time.sleep(delay)
