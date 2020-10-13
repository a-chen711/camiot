from mpu6050 import mpu6050
sensor = mpu6050(0x68)

import time
#from training import classifier
from joblib import dump,load
import numpy as np

classifier = load ('/home/pi/Desktop/trigger/triggerTrain.joblib')

def imuTri():
  imuData = open("imuPredictData.csv","a")
  
  active = True
  counter = 0
  label = ""
  data= []
  print("Start recording")
  while active:
        #print("recording data")
        '''
        imuData.write("\n")
        imuData.write(label)
        imuData.write(", ")
        imuData.write(str(counter))
        imuData.write(", ")
        startTime=time.time()
        '''
        while len(data) < 42 : 
            accel_data = sensor.get_all_data()[0]
           # gyro_data = sensor.get_all_data()[1]
  
            data.append(accel_data['x'])
            data.append(accel_data['y'])
            data.append(accel_data['z'])
            '''
            data.append(gyro_data['x'])
            data.append(gyro_data['y'])
            data.append(gyro_data['z'])
            '''
            time.sleep(0.1)
        #data.pop()
        #data.pop()
        #data.pop()
        #data.pop()
        #data.pop()
        #data.remove(data[0])
        #print("Initial shape of data: " ,len(data))
        newData=np.reshape(data,(1,-1))
        #print("new Size ",newData.shape)
        result = classifier.predict(newData)
        print(result)
        if result:
            print("good job!")
            for k in range (15):
                data.pop(0)
        else:
            for k in range(6):
                data.pop(0)
        #data.clear()

while True:
  imuTri()
#imuTri()
