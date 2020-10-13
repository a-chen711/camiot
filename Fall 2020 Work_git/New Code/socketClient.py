#Here goes the client code 

import cv2
import numpy as np
import socket
import pickle
import struct ### new code

import sys
sys.path.insert(1, '/trigger/')

from newTrigger import trigger 

state=0 # 0= object detection 1=finger interaction
app_arr = ['lamp','tv','coffee maker','toaster','printer']

clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect(('192.168.1.18',8200))

# sc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# sc.connect(('192.168.1.108',8081))

#state=clientsocket.recv(4).decode()
print(state)

while True:
	cap=cv2.VideoCapture(0)
	if state ==0:	
		if input('Press Enter') == '':
    		ret,frame=cap.read()
    		#cv2.imwrite('frame.jpg', frame)
    		#frame = cv2.imread('frame7.jpg')
    		data = pickle.dumps(frame) ### new code
    		clientsocket.sendall(struct.pack("<L", len(data))+data) ### new code
    		state = 1
    cap.release()

'''
    if state ==1:
    	clientsocket.listen
'''