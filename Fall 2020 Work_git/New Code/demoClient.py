#Here goes the client code 

import logging
import cv2
import numpy as np
import socket
import pickle
import pyttsx3
import struct
from datetime import datetime
import time
import sys
from newTriggerv2 import trigger

# TODO: double check
from finger_direction_9_25_v2 import *

def get_time():
	now = datetime.now()
	dt_string = now.strftime("%d.%m.%Y_%H.%M.%S")
	return dt_string	

state=0 # 0= object detection 1=finger interaction
engine = pyttsx3.init()
engine.setProperty('rate', 150) #slowing speech rate
engine.setProperty('volume', 5.0)
# clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# clientsocket.connect(('192.168.1.9',8200))

prev_opt = None
cap=cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
# sc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# sc.connect(('192.168.1.18',8081))
choice = input('Which appliance? 0 = fireplace, 1 = lamp, 2 = rice cooker')
choice = int(choice)
appliances = ['fireplace', 'lamp', 'rice cooker']

#state=clientsocket.recv(4).decode()
print('Beginning Loop')
while True:
	if trigger():
		print("TRIGGERED")
		######
		#APPLIANCE RECOGNITION 640*480 IMAGE SIZE
		######
		ret,frame=cap.read()
		cv2.imwrite('appliance_{}.jpg'.format(get_time()), frame)
		# data = pickle.dumps(frame) 
		# clientsocket.sendall(struct.pack("<L", len(data))+data) ### Send appliance picture to the server

		#listen for appliance type here: TODO
		# data = clientsocket.recv(4096) #['toaster', 'tv', 'printer', 'lamp', 'coffeemaker']
		# appliance_list = pickle.loads(data)
		# print(appliance_list)
		engine.say(appliances[choice] + ' selected')
		engine.runAndWait()# '{} selected'.format(toaster)
		#print('Finger detection starting')
		i = 0
		while i < 30:
			print('i = ' + str(i))
			ret,frame=cap.read()
			cv2.imwrite('finger_{}.jpg'.format(time.time()), frame)
			width = int(frame.shape[1] * 0.5)
			height = int(frame.shape[0] * 0.5)
			dim = (width, height)
			frame = cv2.resize(frame, dim) #downsample the image for finger detection

			angle=finger_recognition(frame)
			print('Finger angle is ' + str(angle) + '. Time is ' + str(time.time()))

			c_opt = None
			if i == 24 or angle == None:
				print("Gesture confirmed")
				# audio the function selected
				engine.say('Function Confirmed')
				engine.runAndWait()
				break
			if (angle != None and i == 10):
				if (angle >= 5.):
					if choice == 0:
						c_opt = 'fireplace on'
					elif choice == 1:
						c_opt = 'lamp off'
					elif choice == 2:
						c_opt='Rice cooker on'
				elif (angle < 5.):
					if choice == 0:
						c_opt = 'fireplace on'
					elif choice == 1:
						c_opt = 'lamp off'
					elif choice == 2:
						c_opt='Rice cooker on'
				if prev_opt == None:
					prev_opt = c_opt
					# audio the function selected
					engine.say(c_opt)
					engine.runAndWait()
				else:
					if prev_opt == c_opt:
						pass
					else:
						prev_opt = c_opt
						# audio the function selected
						engine.say(c_opt)
						engine.runAndWait()		
			i += 1
		break
cap.release()
