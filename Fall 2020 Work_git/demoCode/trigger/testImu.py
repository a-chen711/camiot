from mpu6050 import mpu6050
sensor = mpu6050(0x68)

import time
from training import classifier
import numpy as np

imuData = open("imuPredictData.csv","a")

active = True
counter = 0
label = ""
data= []
while active:
    userInput=input("Enter E to exit otherwise P for predicting if the  gesture is triggering: \n")
    if userInput == "E":
        active=False
    else: 
        print("recording data")
        '''
        imuData.write("\n")
        imuData.write(label)
        imuData.write(", ")
        imuData.write(str(counter))
        imuData.write(", ")
        startTime=time.time()
        '''
        while len(data) < 84 : 
            accel_data = sensor.get_all_data()[0]
            gyro_data = sensor.get_all_data()[1]

            data.append(accel_data['x'])
            data.append(accel_data['y'])
            data.append(accel_data['z'])
            
            data.append(gyro_data['x'])
            data.append(gyro_data['y'])
            data.append(gyro_data['z'])
            
            time.sleep(0.1)
        #data.pop()
        #data.pop()
        #data.pop()
        #data.pop()
        #data.pop()
        #data.remove(data[0])
        print("Initial shape of data: " ,len(data))
        newData=np.reshape(data,(1,-1))
        print("new Size ",newData.shape)
        result = classifier.predict(newData)
        print(result)
        data.clear()
















































