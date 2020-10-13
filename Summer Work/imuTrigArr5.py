from mpu6050 import mpu6050
import time


sensor = mpu6050(0x68)
flag_list = []
gyro_axis = 'x'
accel_axis = 'z'
delay = 0.1
sps = int(1/delay) #samples per second

def is_sublist(list1, sublist):
    """Return the index at which the sequence sublist appears in the
    sequence list1, or -1 if it is not found, using the Boyer-
    Moore-Horspool algorithm. The elements of sublist and list1 must
    be hashable.

    >>> find([1, 1, 2], [1, 2])
    1

    """
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
    raise_ind, initial_raise = is_sublist(list_of_flag, raise_list)
    if initial_raise == True and raise_ind >= 0:
        steady_ind, arm_steady = is_sublist(list_of_flag, steady_list)
        if steady_ind == raise_ind + 1 and arm_steady == True: #make sure steady part is right after raise
            return True
    return False

while True:
    if len(flag_list) > sps + 2: #keep size of flag list to a little more than 1 second of samples.
        flag_list.pop(0)
    flag1, flag2, flag3 = 1, 2, 3
    arm_raised = False
    gyroData = sensor.get_gyro_data()
    accelData = sensor.get_accel_data()
    if gyroData[gyro_axis] > 120 and accelData[accel_axis] > 7 \
    or gyroData[gyro_axis] < 20 and accelData[accel_axis] > 10: #raising arm from down, or from on desk
        flag_list.append(flag1)
    # elif gyroData[gyro_axis] < 90 and gyroData[gyro_axis] > 30 and accelData[accel_axis] > 7: #second layer
    #     flag_list.append(flag2)
    elif gyroData[gyro_axis] < 20 and accelData[accel_axis] > 7 and accelData[accel_axis] < 10: #third layer
        flag_list.append(flag3)
    if flag_list[len(flag_list) - 1] == True and len(flag_list) >= sps:
        if check_last_sec(flag_list):
            arm_raised = True
    print("Arm raised: " + str(arm_raised))
    time.sleep(delay)
