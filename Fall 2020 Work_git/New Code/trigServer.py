	#Server code for demo May 6th 



#Server code for demo May 6th 
import socket
import sys
#import cv2
import pickle
import numpy as np
import time
from serverFunctions import *
# from finger_direction_4_20 import *
from threading import Thread 
from subprocess import call

s0,conn0,add0=create_connection(PORT=8200)
time.sleep(1)

counter = 0
#wait until the connection is created
#welcome_msg()

while True:
	msg='0'
	frame=picRecv(conn0,0,counter=0)
	name = '/Users/Alex Chen/Desktop/Test_photos/frame' + str(counter) + '.jpg'
	cv2.imwrite(name, frame)
	print('frame' + str(counter) + ' has been saved')
	counter += 1