import io
import socket
import struct
import time
import testImuConNew
from  testImuConNew import imuTri 
from mpu6050 import mpu6050
sensor = mpu6050(0x68)
from joblib import dump,load
import numpy as np

#classifier = load ('/home/pi/Desktop/trigger/triggerTrain.joblib')

imuData = open("imuPredictData.csv","a")

label = ""
data= []
resList=[]
#global result
#global resData






##########Server SetUp
#channel = input('channel: ')
channel=4040

while True:
    print("port: ",channel)
    time.sleep(3)
    tSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    connected=False
    while not connected:
        try:
            tSocket.connect(('192.168.1.67', int(channel)))
            connected=True
        except Exception as e:
            pass



    #channel=channel+1
    try:
        while True:
            imuTri()
    
            
    finally:
        print("Closing the connection")
        tSocket.close()

