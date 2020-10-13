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
from newTrigger import trigger

# TODO: double check
from finger_direction_9_25_v2 import *

CLASS_MAP = {
    0: 'fireplace',
    1: 'kettle',
    2: 'microwave',
    3: 'oven',
    4: 'piano',
}
USER_NAME = input('What is your name? ')

def get_time():
	now = datetime.now()
	dt_string = now.strftime("%d.%m.%Y_%H.%M.%S")
	return dt_string	

logging.basicConfig(filename='{}_{}.log'.format(USER_NAME, get_time()),level=logging.DEBUG)

state=0 # 0= object detection 1=finger interaction
engine = pyttsx3.init()
engine.setProperty('rate', 100) #slowing speech rate
clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect(('192.168.1.9',8200))

prev_opt = None

# sc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# sc.connect(('192.168.1.18',8081))

#state=clientsocket.recv(4).decode()
print('Beginning Loop')
while True:
	if state ==0:	
		cap=cv2.VideoCapture(0)
		if input('Press Enter') == '':#trigger():
			print("TRIGGERED")
			logging.info('{}, {}'.format('start', get_time()))
			######
			#APPLIANCE RECOGNITION 640*480 IMAGE SIZE
			######
			time.sleep(3)
			ret,frame=cap.read()
			cv2.imwrite('appliance_{}.jpg'.format(get_time()), frame)
			data = pickle.dumps(frame) 
			clientsocket.sendall(struct.pack("<L", len(data))+data) ### Send appliance picture to the server

			#listen for appliance type here: TODO
			data = clientsocket.recv(4096) #['toaster', 'tv', 'printer', 'lamp', 'coffeemaker']
			appliance_list = pickle.loads(data)
			print(appliance_list)
			engine.say(appliance_list[0] + ' selected')
			engine.runAndWait()# '{} selected'.format(toaster)
			logging.info('{}, {}, {}'.format('appliance recognized: ', appliance_list, get_time()))

			#if appliance is found then change state
			if input('*APPLIANCE FOUND* Press enter') == '': ##CHANGE## 
				state = 1
		cap.release()
	if state == 1: #Finger Detection 320*240 IMAGE SIZE
		cap=cv2.VideoCapture(0)
		ret,frame=cap.read()
		width = int(frame.shape[1] * 0.5)
		height = int(frame.shape[0] * 0.5)
		dim = (width, height)
		frame = cv2.resize(frame, dim) #downsample the image for finger detection
		cv2.imwrite('finger_{}.jpg'.format(time.time()), frame)

		angle=finger_recognition(frame)
		# print('Finger angle is ' + str(angle))

		c_opt = None
		if (angle != None):
			if (angle >= 4.):
				c_opt='left'
			elif (angle <= -20.):
				c_opt='right'
			elif (angle>-20) and (angle<4.):
				c_opt='middle'

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

		else: #if no finger found
			print("User confirmed")
			logging.info('{}, {}, {}'.format('function confirmed', prev_opt, time.time()))
			# audio the function selected
			engine.say(c_opt)
			engine.runAndWait()
			break
		# state = 0
		cap.release()


#gesture recognition (Onboard)
#after this triggers, activate appliance recognition (Server)
#after, activate finger interaction (Onboard)