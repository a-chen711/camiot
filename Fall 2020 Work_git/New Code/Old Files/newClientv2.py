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
# c=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# c.connect(('192.168.1.108',8080))

# sc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# sc.connect(('192.168.1.108',8081))

# state=clientsocket.recv(4).decode()
# print(state)
print('Beginning Loop')
i = 0
while True:
	cap=cv2.VideoCapture(0)
	if state ==0:	
		if input('Press x') == 'x':
		#trigger():
			print("TRIGGERED")
			engine.say('Gesture Recognized. Recording Data')
			engine.runAndWait()
			######
			#APPLIANCE RECOGNITION
			######

			#Finger Detection

			ret,frame=cap.read()
			#data = pickle.dumps(frame) ### new code
			imgName = 'frame' + str(i) + '.jpg'
			cv2.imwrite(imgName, frame)
			print('done saving frame')
			finger_flag,angle=finger_recognition(imgName)
			print(finger_flag,angle)

			if (finger_flag):
				if (angle > 4):
					c_opt='left'
				elif (angle < -20):
					c_opt='right'
				elif (angle>-20) and (angle<5):
					c_opt='middle'
			print(c_opt)
			i += 1
	cap.release()
# clientsocket.sendall(struct.pack("<L", len(data))+data) ### new code


#gesture recognition (Onboard)
#after this triggers, activate appliance recognition (Server)
#after, activate finger interaction (Onboard)