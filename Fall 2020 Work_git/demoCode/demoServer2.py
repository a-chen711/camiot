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

import datetime
# voice command init
engine = pyttsx3.init()

# 0= object detection 1=finger interaction
state = 0
result_items=['lamp','tv','Coffee Maker','Toaster','Printer']
result_prob=[]
obj_num=0






s0,conn0,add0=create_connection(PORT=1200)
time.sleep(1)


now = datetime.datetime.now()
print ("Current date and time : ")
print (now.strftime("%Y-%m-%d %H:%M:%S"))
conn0.sendall(b'1')
data=conn0.recv(1)

now = datetime.datetime.now()
print ("Current date and time : ")
print (now.strftime("%Y-%m-%d %H:%M:%S"))
print(data)
