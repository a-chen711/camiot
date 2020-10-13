	#Server code for demo May 6th 



#Server code for demo May 6th 
import socket
import sys
import cv2
import pickle
import numpy as np
import struct ## new
import time
import pyttsx3
import serverFunctions
from serverFunctions import *
from engine_simple_infer_STANDARD_VGG_classification import *
# from finger_direction_4_20 import *
from threading import Thread 
from subprocess import call



# voice command init
engine = pyttsx3.init()

# 0= object detection 1=finger interaction
state = 0
#result_items=['lamp','tv','coffee maker','toaster','printer']
result_prob=[]
obj_num=0
msg='0'  
counter=1
p_opt=""
c_opt=""
angle=0
appliance=""
#finger_flag=False
counter2=0


'''
msg='0' --> first stage to take pic and do the detection
msg='1' --> toggle to the next item
msg='2' --> moving to the finger interaction part 
msg='3' --> going back to the beginning of the loop (take pic for obj detection)
'''
s0,conn0,add0=create_connection(PORT=8200)
time.sleep(1)

#wait until the connection is created
welcome_msg()











while True :
	msg='0'
	imgName=picRecv(conn0,0,counter=counter2)
	time.sleep(0.5)
	result_prob, result_items=appliance_recognition(imgName)	
	appliace=result_items[obj_num]

	#call(["python3", "speak.py", appliace])
	speak2(appliace)
	#engine.say(appliace)
	#engine.runAndWait()
	print(result_items)
	counter2=counter2+1
	pack=result_items[0]+','+result_items[1]+','+result_items[2]+','+result_items[3]+','+result_items[4]
	print(pack)

	pack=pack.encode('utf-8')
	conn0.sendall(pack)	

	while (msg == '0'):
		msg=conn0.recv(1)
		msg=msg.decode('utf-8')
		if (msg == '1'):
			obj_num=obj_num+1
			appliace=result_items[obj_num]
			#engine.say(appliace)
			#engine.runAndWait()
			#call(["python3", "speak.py", appliace])
			speak2(appliace)
			msg='0'
		elif (msg == '2'):
			#engine.say('select options')
			#engine.runAndWait()
			#call(["python3", "speak.py", 'Select options'])
			speak2(appliace)
	conn0.sendall(b'1')

	# while(msg == '2'):
	# 	conn0.sendall(b'4')
	# 	imgName=picRecv(conn0,1,counter=counter)
	# 	counter=counter+1

	# 	finger_flag,angle=finger_recognition(imgName)
	# 	#print(finger_flag,angle)

	# 	if (finger_flag):
	# 		if (angle > 5):
	# 			c_opt='left'
	# 		elif (angle < -20):
	# 			c_opt='right'
	# 		elif (angle>-20) and (angle<5):
	# 			c_opt='middle'
	# 		print(c_opt)
	# 		if (c_opt != p_opt):
	# 			appCall(appliace,c_opt)
	# 			#engine.say(c_opt)
	# 			#engine.runAndWait()

	# 	elif (not finger_flag and p_opt != ""):
	# 		option=p_opt
	# 		#print(p_opt)
	# 		s=time.time()
	# 		#engine.say('confirmed')
	# 		#engine.runAndWait()
	# 		#call(["python3", "speak.py", 'confirmed'])
	# 		speak2('confirmed')
	# 		#appCall(appliace,option)
	# 		conn0.sendall(b'5')
	# 		msg='0'
	# 	p_opt=c_opt
		
		

