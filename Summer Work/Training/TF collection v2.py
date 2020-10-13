from mpu6050 import mpu6050
import random
import time

sensor = mpu6050(0x68)


def countdown(current_flag):
    print('\n')

    print(f'Start ** {current_flag} ** gesture in...')

    for i in range(0, 3):
        print(i)
        time.sleep(0.5)
    print('\n')
    print('recording data...')


num_data_points = 0
num_true_input = 0

num_data_points = int(input('Tell us the number of data points to record:'))
gesture_input = input('Tell us what kind of gesture will be recorded [Raise/Roll/False]:')

gesture_flag = gesture_input

file_name = "imuData-8-7-20-" + str(gesture_flag) + ".txt"

imuData = open(file_name, "a")

imuData.write('aX,aY,aZ,gX,gY,gZ')
imuData.write('\n')

for i in range(0, num_data_points):
    print('\n')
    print(f"{gesture_flag} gesture #{i}")

    countdown(gesture_flag)

    startTime = time.time()

    while (time.time() - startTime) < 2.7:
        accel_data = sensor.get_accel_data()
        gyro_data = sensor.get_gyro_data()

        imuData.write(str(accel_data['x']))
        imuData.write(", ")
        imuData.write(str(accel_data['y']))
        imuData.write(", ")
        imuData.write(str(accel_data['z']))
        imuData.write(", ")

        imuData.write(str(gyro_data['x']))
        imuData.write(", ")
        imuData.write(str(gyro_data['y']))
        imuData.write(", ")
        imuData.write(str(gyro_data['z']))
        imuData.write("\n")

        time.sleep(0.1)
