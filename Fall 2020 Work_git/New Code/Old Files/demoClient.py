#Here goes the client code 

import cv2
import numpy as np
import socket
import pickle
import struct ### new code

import sys
sys.path.insert(1, '/trigger/')

from testImuCon import trigger 

state=0 # 0= object detection 1=finger interaction

cap=cv2.VideoCapture(0)
c=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
c.connect(('192.168.1.18',8080))

# sc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# sc.connect(('192.168.1.108',8081))

state=clientsocket.recv(4).decode()
print(state)

while True:

	if state ==0:	
		if trigger():
    		ret,frame=cap.read()
    		data = pickle.dumps(frame) ### new code
    		clientsocket.sendall(struct.pack("<L", len(data))+data) ### new code
