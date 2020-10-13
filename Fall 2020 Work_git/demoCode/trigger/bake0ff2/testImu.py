from mpu6050 import mpu6050
sensor = mpu6050(0x68)

import time
#from training import classifier
from joblib import dump,load
import numpy as np

import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
from time import sleep     # Import the sleep function from the time module
GPIO.setwarnings(False)    # Ignore warning for now
GPIO.setmode(GPIO.BOARD)   # Use physical pin numbering
GPIO.setup(32, GPIO.OUT, initial=GPIO.LOW)


classifier = load ('/home/pi/Desktop/trigger/triggerTrain.joblib')

imuData = open("imuPredictData.csv","a")

label = ""
data= []
resData=[]
def predictMe():
    data=[]
    GPIO.output(32, GPIO.HIGH)
    print("Recording data in 2 secs ...")
    time.sleep(.5)
    GPIO.output(32, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(32, GPIO.HIGH)
    print("Recoring data in 1 sec ...")
    time.sleep(0.5)
    GPIO.output(32, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(32, GPIO.HIGH)
    print("Now recoring data")

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
    resData=data
    result=str(result)
    resData.append(result)
    #print(resData)
    #data.clear()
    GPIO.output(32, GPIO.LOW)
    return resData


while True:
    predictMe()
