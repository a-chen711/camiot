from mpu6050 import mpu6050
import time

def is_sublist(list1, sublist):
    h = len(list1)
    n = len(sublist)
    skip = {sublist[i]: n - i - 1 for i in range(n - 1)}
    i = n - 1
    while i < h:
        for j in range(n):
            if list1[i - j] != sublist[-j - 1]:
                i += skip.get(list1[i], n)
                break
        else:
            return i - n + 1, True
    return -1, False

def check_last_sec(list_of_flag):
    raise_list = [1, 3, 3] #fnd the initial raise
    steady_list = [3, 3, 3, 3, 3, 3] #find the steady part
    initial_raise = False
    arm_steady = False
    raise_ind, initial_raise = is_sublist(list_of_flag, raise_list) #find the raise arm pattern
    if initial_raise == True and raise_ind >= 0:
        steady_ind, arm_steady = is_sublist(list_of_flag, steady_list) #find the steady arm pattern
        if steady_ind == raise_ind + 1 and arm_steady == True: #make sure steady part is right after raise
            return True
    return False

def trigger(flag_list, delay, sps):
    sensor = mpu6050(0x68)
    gyro_axis = 'x'
    accel_axis = 'z'

    flag1, flag2, flag3 = 1, 2, 3
    arm_raised = False
    gyroData = sensor.get_gyro_data()
    accelData = sensor.get_accel_data()
    if gyroData[gyro_axis] > 120 and accelData[accel_axis] > 7: #first layer of threshold
        flag_list.append(flag1)
    # elif gyroData[gyro_axis] < 90 and gyroData[gyro_axis] > 30 and accelData[accel_axis] > 7: #second layer
    #     flag_list.append(flag2)
    elif gyroData[gyro_axis] < 20 and accelData[accel_axis] > 7: #third layer
        flag_list.append(flag3)
    if len(flag_list) >= sps:
        if check_last_sec(flag_list):
            arm_raised = True
    return arm_raised
    time.sleep(delay)