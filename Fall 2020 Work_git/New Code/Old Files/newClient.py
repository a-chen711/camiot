#Here goes the client code 

import cv2
import numpy as np
import socket
import pickle
import struct ### new code
import pyttsx3

import sys
from newTrigger import trigger
from finger_direction_4_20 import *

state=0 # 0= object detection 1=finger interaction
engine = pyttsx3.init()
engine.setProperty('rate', 150) #slowing speech rate
cap=cv2.VideoCapture(0)
# c=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# c.connect(('192.168.1.108',8080))

# sc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# sc.connect(('192.168.1.108',8081))

# state=clientsocket.recv(4).decode()
# print(state)
print('Beginning Loop')
while True:
	if state ==0:	
		if trigger():
			print("TRIGGERED")
			engine.say('Gesture Recognized. Recording Data')
			engine.runAndWait()
			######
			#APPLIANCE RECOGNITION
			######

			#Finger Detection

			ret,frame=cap.read()
			data = pickle.dumps(frame) ### new code
			cv2.imwrite('frame.jpg', frame)
			print('done')

# clientsocket.sendall(struct.pack("<L", len(data))+data) ### new code


#gesture recognition (Onboard)
#after this triggers, activate appliance recognition (Server)
#after, activate finger interaction (Onboard)