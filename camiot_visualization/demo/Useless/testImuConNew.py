from mpu6050 import mpu6050
sensor = mpu6050(0x68)

import time
#from training import classifier
from joblib import dump,load
import numpy as np

import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(32,GPIO.OUT,initial=GPIO.LOW)

classifier = load ('/home/pi/Desktop/trigger/triggerTrain.joblib')

def imuTri():
  imuData = open("imuPredictData.csv","a")
  #GPIO.output(32,GPIO.HIGH)

  active = True
  counter = 0
  label = ""
  data= []
  state=0
  pState=0
  print("Recording Data")
  while active:
        GPIO.output(32,GPIO.LOW)
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
        newData=np.reshape(data,(1,-1))
        result = classifier.predict(newData)
        result=str(result)
        print(result)

        if result=='[ True]':
            GPIO.output(32,GPIO.HIGH)
            time.sleep(.5)
            print("True")
            GPIO.output(32,GPIO.LOW)
          return True
        	
        GPIO.output(32,GPIO.LOW)
        if result =='[ True]':
            data.clear()
        else:
            for k in range(9):
                data.pop(0)
        result=""
        #data.clear()

if __name__ == '__main__':
	while True:
	  imuTri()
	#imuTri()
