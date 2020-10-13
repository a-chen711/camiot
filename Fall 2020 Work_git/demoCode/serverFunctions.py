#Server code for demo May 6th 
import socket
import sys
import cv2 
import pickle
import numpy as np
import struct ## new
import time
import pyttsx3
from engine_simple_infer_STANDARD_VGG_classification import *
from subprocess import call
from speak2 import v2

engine = pyttsx3.init()
#TV, Printer, Lamp, CoffeeMaker, Toaster

##hard coded values for testing purposes 
resutls = dict([('TV',60),('Printer',20),('Lamp',10),('CoffeeMaker',5),('Toaster',5)])
resutls_list=['TV','Printer','Lamp','CoffeeMaker','Toaster']



#def speak2(text="hi"):
#	tts = _TTS()
#	tts.start(text)
#	del(tts)

def speak2(text='hi'):
	t1=v2()
	t1.start(text)

def create_connection(HOST='192.168.1.18',PORT=8011):
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	print ('Socket created')
	s.bind((HOST,PORT))
	s.listen(10)
	print ('Socket now listening')
	# Accpet the client 
	conn,addr=s.accept()
	print("connected to" ,addr)
	return s,conn,addr

def welcome_msg():
	speak2("Systems ready")
	#call(["python3", "speak.py", "Systems ready"])
	
	#engine = pyttsx3.init()
	#engine.say('Systems ready')
	#engine.runAndWait()





def picRecv(conn,voice=0,counter=0):
	if voice==0:
		#engine = pyttsx3.init()
		#call(["python3", "speak.py", 'Point'])
		speak2('Point')
		#engine.say('Point')
		#engine.runAndWait()

	p1=time.time()
	data = b''
	payload_size = struct.calcsize("<L") 
	while len(data) < payload_size:
		data += conn.recv(8192)
		packed_msg_size = data[:payload_size]
		data = data[payload_size:]
		msg_size = struct.unpack("<L", packed_msg_size)[0]
	while len(data) < msg_size:
		data += conn.recv(8192)
	frame_data = data[:msg_size]
	data = data[msg_size:]
	frame=pickle.loads(frame_data)
	if voice == 0:
		name='/Users/ApplePro/Desktop/School/GradSchool/Research /HCI/camiot/Feb 15/demoCode/data/frameObj'+str(counter)+'.jpg'
	else:
		name='/Users/ApplePro/Desktop/School/GradSchool/Research /HCI/camiot/Feb 15/demoCode/data/frame'+str(counter)+'.jpg'
	cv2.imwrite(name,frame)
	print("recep time" ,time.time()-p1)
	return name



def appCall(appliance,option):

	if appliance == 'tv':
		if option == 'left':
			#engine.say('volume down')
			phrase='volume down'
		elif option == 'right':
			#engine.say('volume up')
			phrase='volume up'
		elif option == 'middle':
			#engine.say('Turn Off')
			phrase='Turn Off'

	elif appliance == 'toaster':
		if option == 'left':
			#engine.say('time remaining')
			phrase='time remaining'
		elif option == 'right':
			#engine.say('Begin taosting')
			phrase='Begin toasting'
		elif option == 'middle':
			#engine.say('Stop toasting')
			phrase='Stop toasting'

	elif appliance == 'lamp':
		if option == 'left':
			phrase='Turn Off'
		elif option == 'right':
			phrase='Turn On'
		elif option == 'middle':
			phrase='dim the light'

	elif appliance == 'printer':
		if option == 'left':
			phrase='Turn Off'
		elif option == 'right':
			phrase='Turn On'
		elif option == 'middle':
			phrase='paper try status'

	elif appliance == 'coffemaker':
		if option == 'left':
			phrase='Latte'
		elif option == 'right':
			phrase='Mocha'
		elif option == 'middle':
			phrase='Start Brewing'
	#call(["python3", "speak.py", phrase])
	speak2(phrase)



class VideoCapture:


    def __init__(self,name):
        self.cap = cv2.VideoCapture(name)
        self.q=queue.Queue()
        t = threading.Thread(target=self._reader)
        t.daemon= True
        t.start()

    def _reader(self):
        while True:
            ret,frame = self.cap.read()
            if not ret:
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()
                except queue.Empty():
                    pass
            self.q.put(frame)

    def read(self):
        return self.q.get()






