import paho.mqtt.publish as publish
import time
import picamera
from gpiozero import Button
import sys
import base64
from imuTri import trigger
import socket

from testImuConNew import imuTri

strbroker = "192.168.1.26"
server_ip = '192.168.1.25'

tSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tSocket.connect((server_ip, 8000))

try:
    camera = picamera.PiCamera()
    camera.resolution = (224,224)
#    camera.color_effects = (128,128)
    # Start a preview and let the camera warm up for 2 seconds
    camera.start_preview()
    time.sleep(2)
    
    while True:
        takePic=0
        time.sleep(1)
        # wait for input command
        print('Now take a picture.')
        
        imuTri()
        time.sleep(0.2)
        print('taking photos...\n')
        info = 'rec'
        
        camera.color_effects = None
        camera.resolution = (224,224)
        for num in range(1):
            camera.capture('1.png')
            with open("1.png", "rb") as img_file:
                my_string = base64.b64encode(img_file.read())
                #print(len(my_string)) 
            publish.single("image", my_string ,hostname = strbroker)
            time.sleep(0.1)
        info = 'rec'
        tSocket.sendall(info.encode('utf-8'))
        
        print('move to the selection part.')
        select=0
        info_counter = -15
        
        while True:
            if trigger(3) == False:
                print('selecting')
                info = 'ACK'
                tSocket.sendall(info.encode('utf-8'))
                break
            else:
                print('changing')
                info = 'NI'
                tSocket.sendall(info.encode('utf-8'))
                time.sleep(0.5)
       
        print("Done!")
        print("taking photo for finger control place your finger in position")
        time.sleep(.5)
        
        inAck = tSocket.recv(1024)
        inAck = inAck.decode()
        print(inAck)

        info = 'con'
        t1 = time.time()
        camera.resolution = (80,80)
        for num in range(80):
            print(time.time()-t1)
            t1 = time.time()
            camera.capture('2.png')
            with open("2.png", "rb") as img_file:
                my_string = base64.b64encode(img_file.read())
            print('wait for responce')
            inAck = tSocket.recv(1024)
            inAck = inAck.decode()
            print(inAck)

            publish.single("image", my_string ,hostname = strbroker)
            tSocket.sendall(info.encode('utf-8'))
            
            #time.sleep(.5)
            if inAck == 'Stop Con.':
                break
        print('Done')
    

finally:
    tSocket.close()