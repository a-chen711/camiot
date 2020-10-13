from mpu6050 import mpu6050
sensor = mpu6050(0x68)

import time
#from training import classifier
from joblib import dump,load
import numpy as np

classifier = load ('/home/pi/Desktop/camiot/Feb15/demoCode/rotation_trigger/triggerTrain25-4.joblib')

def trigger():
  
  active = True
  counter = 0
  label = ""
  data= []
  print("Recording Data")
  while active:
        '''
        imuData.write("\n")
        imuData.write(label)
        imuData.write(", ")
        imuData.write(str(counter))
        imuData.write(", ")
        startTime=time.time()
        '''
        while len(data) < 30 : 
            gyro_data = sensor.get_all_data()[1]
  
            
            data.append(gyro_data['x'])
            data.append(gyro_data['y'])
            data.append(gyro_data['z'])
            
            time.sleep(0.1)
        newData=np.reshape(data,(1,-1))
        #print("new Size ",newData.shape)
        result = classifier.predict(newData)
        return result
#while True:
 # imuTri()
#imuTri()
