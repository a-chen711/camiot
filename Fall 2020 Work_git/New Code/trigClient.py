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

state=0 # 0= object detection 1=finger interaction
engine = pyttsx3.init()
engine.setProperty('rate', 150) #slowing speech rate
# clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# clientsocket.connect(('192.168.1.8',8200))

p_opt = None

# sc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# sc.connect(('192.168.1.18',8081))

#state=clientsocket.recv(4).decode()
cap=cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
print('Beginning Loop')
counter = 0
if input('Press enter') == '':
	while counter <= 10:
		if state ==0:	
			if True:#trigger():
				print("TRIGGERED")
				prevtime = time.time()

				ret,frame=cap.read()
				width = int(frame.shape[1] * 0.5)
				height = int(frame.shape[0] * 0.5)
				dim = (width, height)
				frame = cv2.resize(frame, dim) #downsample the image for finger detection
				#data = pickle.dumps(frame) 
				#clientsocket.sendall(struct.pack("<L", len(data))+data) ### Send appliance picture to the server
				angle=finger_recognition(frame)
				curtime = time.time()
				print('Time for capture and recognition = ' + str(curtime-prevtime))
				cv2.imwrite('frame' + str(counter) + '.jpg', frame)
				# print('Finger angle is ' + str(angle))

				# c_opt = None
				# if (angle != None):
				# 	if (angle >= 4.):
				# 		c_opt='left'
				# 	elif (angle <= -18.):
				# 		c_opt='right'
				# 	elif (angle>-18) and (angle<4.):
				# 		c_opt='middle'
				# 	print('c_opt is ' + c_opt)
				# 	if p_opt == None:
				# 		p_opt = c_opt
				# 		# audio the function selected
				# 		engine.say(c_opt)
				# 		engine.runAndWait()
				# 		print('1')
				# 	else:
				# 		print('p_opt is ' + p_opt)
				# 		if p_opt == c_opt:
				# 			pass
				# 		else:
				# 			p_opt = c_opt
				# 			# audio the function selected
				# 			engine.say(c_opt)
				# 			engine.runAndWait()
				# 			print('2')

				# else: #if no finger found
				# 	print("User confirmed")
				# 	# audio the function selected
				# 	engine.say(c_opt)
				# 	engine.runAndWait()
				# 	print('3')
				# 	break
				# # state = 0
			counter += 1
cap.release()

#gesture recognition (Onboard)
#after this triggers, activate appliance recognition (Server)
#after, activate finger interaction (Onboard)