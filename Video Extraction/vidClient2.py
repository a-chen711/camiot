import io
import cv2
import numpy as np
import socket
import sys
import pickle
import struct ### new code



# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.1.25', 8200))
import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(29,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(36,GPIO.OUT,initial=GPIO.LOW)



GPIO.output(29,GPIO.HIGH)
GPIO.output(36,GPIO.HIGH)
cap = cv2.VideoCapture(0)
i = 0
start = time.time()
while True:
    ret,frame=cap.read()
    if i%10 == 0:
        data = pickle.dumps(frame)
        client_socket.sendall(struct.pack("package", len(data)) + data)
    stop = time.time()
    if (stop - start) > 5:
        break
    i += 1
GPIO.output(29,GPIO.LOW)
GPIO.output(36,GPIO.LOW)