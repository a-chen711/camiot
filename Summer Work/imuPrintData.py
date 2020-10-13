from mpu6050 import mpu6050
import time

sensor = mpu6050(0x68)

while True:
    gyroData = sensor.get_gyro_data()
    accelData = sensor.get_accel_data()
    print('Gyro: ', gyroData, 'Accel: ', accelData)
    time.sleep(0.1)
