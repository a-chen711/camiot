import io
import socket
import struct
import time
import testImu
from testImu import predictMe
from mpu6050 import mpu6050
sensor = mpu6050(0x68)
from joblib import dump,load
import numpy as np

classifier = load ('/home/pi/Desktop/trigger/triggerTrain.joblib')

imuData = open("imuPredictData.csv","a")

label = ""
data= []
resList=[]
#global result
#global resData


'''def predictMe():
    resList=[]
    data=[]
    print("Recording data in 2 secs ...")
    time.sleep(1)
    print("Recoring data in 1 sec ...")
    time.sleep(1)
    print("Now recoring data")

    while len(data) < 42 :
        accel_data = sensor.get_all_data()[0]
        # gyro_data = sensor.get_all_data()[1]
        data.append(accel_data['x'])
        data.append(accel_data['y'])
        data.append(accel_data['z'])

    
        #data.append(gyro_data['x'])
        #data.append(gyro_data['y'])
        #data.append(gyro_data['z'])
        
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
    resList.append(result)
    resList.append(data)
    data.clear()
    print("in function ", resList)
    return resList ''' 












##########Server SetUp
#channel = input('channel: ')
channel=2020

while True:
    print("port: ",channel)
    time.sleep(3)
    tSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    connected=False
    while not connected:
        try:
            tSocket.connect(('192.168.0.167', int(channel)))
            connected=True
        except Exception as e:
            pass


    active = 1
    #channel=channel+1
    try:
        while active == 1:
            trigger=tSocket.recv(1024).decode()
            if trigger == '1':
                ansList=predictMe()
                print("ansList:")
                print(ansList)
            
                ansListS=str(ansList)
                ansListB=bytearray(ansListS,'utf-8')
                tSocket.send(ansListB)
                #tSocket.send(b'2')
            
            elif trigger == '0':
                #msg="closing the connection"
                #tSocket.send(bytearray(msg,'utf-8'))
                active=0
    finally:
        print("Closing the connection")
        tSocket.close()

