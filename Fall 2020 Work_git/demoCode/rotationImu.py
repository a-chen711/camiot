from mpu6050 import mpu6050
sensor = mpu6050(0x68)

import time

def rotation_trigger(delay=10):
    cur_time = time.time()
    prev_time = cur_time
    while True:
        cur_time = time.time()
        if cur_time - prev_time > delay:
            return False
        else:
            accelerometer_data = sensor.get_all_data()[0]
            gyroscope_data = sensor.get_all_data()[1]

            time.sleep(0.25)
            accelerometer_data = sensor.get_all_data()[0]
            gyroscope_data = sensor.get_all_data()[1]
            if abs(gyroscope_data['y']) > 220:
                return True

while True:
    print(rotation_trigger(2))
