#Here goes the client code 

import cv2
import numpy as np
import socket
import pickle
import struct ### new code
import pyttsx3

import sys
from newTrigger import trigger
from finger_direction_9_25_v2 import *

state=0 # 0= object detection 1=finger interaction
engine = pyttsx3.init()
engine.setProperty('rate', 150) #slowing speech rate
# clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# clientsocket.connect(('192.168.1.18',8200))

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
			#APPLIANCE RECOGNITION 640*480 IMAGE SIZE
			######

			#Finger Detection 320*240 IMAGE SIZE

			ret,frame=cap.read()
			# data = pickle.dumps(frame) ### new code
			# clientsocket.sendall(struct.pack("<L", len(data))+data) ### new code

			width = int(frame.shape[1] * 0.5)
			height = int(frame.shape[0] * 0.5)
			dim = (width, height)
			frame = cv2.resize(frame, dim) #downsample the image for finger detection

			imgName = 'frame.jpg'
			cv2.imwrite(imgName, frame)
			print('done saving frame')

			angle=finger_recognition(frame)
			print(angle)

			c_opt = ''
			if (angle != None):
				if (angle > 4):
					c_opt='left'
				elif (angle < -20):
					c_opt='right'
				elif (angle>-20) and (angle<5):
					c_opt='middle'
			print(c_opt)
			i += 1
	cap.release()


#gesture recognition (Onboard)
#after this triggers, activate appliance recognition (Server)
#after, activate finger interaction (Onboard)