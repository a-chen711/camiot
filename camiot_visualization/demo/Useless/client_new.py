import io
from joblib import load
import socket
import struct
import time
import picamera
from gpiozero import Button
import sys
import base64
from imuTri import trigger
#sys.path.append('/home/pi/Desktop/trigger/')
from testImuConNew import imuTri

#from mpu6050 import mpu6050
#sensor = mpu6050(0x68)

channel = input('channel: ')
#channel2 = input('channel2: ')

# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
client_socket = socket.socket()
client_socket.connect(('192.168.1.36', int(channel)))
#client_socket.connect(('192.168.0.246', int(channel)))
#client_socket.connect(('192.168.0.167', int(channel)))

# Make a file-like object out of the connection
connection = client_socket.makefile('wb')
time.sleep(3)
tSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tSocket.connect(('192.168.1.36', int(channel)+10))

try:
    camera = picamera.PiCamera()
    camera.resolution = (224,224)
#    camera.color_effects = (128,128)
    # Start a preview and let the camera warm up for 2 seconds
    camera.start_preview()
    time.sleep(2)

    # Note the start time and construct a stream to hold image data
    # temporarily (we could write it directly to connection but in this
    # case we want to find out the size of each capture first to keep
    # our protocol simple)
    # start = time.time()
    
    while True:
        takePic=0
        time.sleep(1)
        # wait for input command
        print('To take picture twist your wrist twice and point at your object')
        # trigger()
        imuTri()
        time.sleep(0.2)
        print('taking photos...\n')
        
        info = 'Rec'
        tSocket.sendall(info.encode('utf-8'))
        camera.color_effects = None
        camera.resolution = (224,224)
        for num in range(1):
            camera.capture('1.jpeg')
            # Write the length of the capture to the stream and flush to
            # ensure it actually gets sent
            with open("1.jpeg", "rb") as img_file:
                my_string = base64.b64encode(img_file.read())
                print(len(my_string)) 
            connection.write(my_string)
           
            # let the camera wait for a while, not sure if necessary
            time.sleep(0.1)
        # debounce
        # info="ACK"
	# print("sending info")
        #tSocket.sendall(info.encode('utf-8'))
        print('Done!')
        
        print('move to the selection part.')
        select=0
        info_counter = -15
        #time.sleep(1)
        
        while True:
            if trigger(1.5) == False:
                print('selecting')
                info = 'ACK'
                tSocket.sendall(info.encode('utf-8'))
                break
            else:
                print('changing')
                info = 'NI'
                tSocket.sendall(info.encode('utf-8'))
                time.sleep(0.5)
        
#        while select == 0:
#            if info_counter == 0:
#                info = 'NI'
#                tSocket.sendall(info.encode('utf-8'))
#            info_counter += 1
#            if info_counter > 10:
#                info_counter = 0
#            gyro_data = sensor.get_gyro_data()
#            preValue=gyro_data['y']
#            #print("prev",preValue
#            time.sleep(0.25)
#            gyro_data = sensor.get_gyro_data()
#            currValue=gyro_data['y']
#            #print("curr",currValue)
#            diff=preValue-currValue
#            #print(diff)
#            if abs(preValue-currValue)>100:
#            	select = 1
#            	time.sleep(1.2)
#        info = 'ACK'
#        tSocket.sendall(info.encode('utf-8'))
        
#        # time.sleep(2)
        print("Done!")
        print("taking photo for finger control place your finger in position")
        time.sleep(0.6)
        print('recording...')
        # info = 'Con'
        # tSocket.sendall(info.encode('utf-8'))
        camera.color_effects = (128,128)
        camera.resolution = (224,224)
        for num in range(80):

            info = 'Con'
            tSocket.sendall(info.encode('utf-8'))

            camera.capture('2.jpeg')
            # Write the length of the capture to the stream and flush to
            # ensure it actually gets sent
            with open("2.jpeg", "rb") as img_file:
                my_string = base64.b64encode(img_file.read())
            
            connection.write(my_string)
            # let the camera wait for a while, not sure if necessary
            inAck = tSocket.recv(1024)
            inAck = inAck.decode()
            print(inAck)
            if inAck == 'Stop Con.':
                break
            # time.sleep(0.2)
        
        print('Done')
        #inSocket = tSocket.recv(1024)
        #print(inSocket.decode())

    # Write a length of zero to the stream to signal we're done
    connection.write(struct.pack('<L', 0))
finally:
    connection.close()
    client_socket.close()
    tSocket.close()
