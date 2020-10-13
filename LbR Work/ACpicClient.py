import io
import socket
import struct
import time
import picamera



# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
client_socket = socket.socket()
client_socket.connect(('192.168.1.25', 8000))
import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(29,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(36,GPIO.OUT,initial=GPIO.LOW)





# Make a file-like object out of the connectio
connection = client_socket.makefile('wb')
try:
    with picamera.PiCamera() as camera:
        camera.resolution = (480, 480)
        camera.framerate = 30
        # Start a preview and let the camera warm up for 2 seconds
        GPIO.output(29,GPIO.HIGH)
        GPIO.output(36,GPIO.HIGH)
        camera.start_preview()
       # camera.exposure_mode = 'nightpreview'
        time.sleep(2)

        start = time.time()
        camera.start_recording(connection, format = 'h264')
        camera.waitrecording(5)
        camera.stop_recording()
        GPIO.output(29,GPIO.LOW)
        GPIO.output(36,GPIO.LOW)
    # Write a length of zero to the stream to signal we're done
    connection.write(struct.pack('<L', 0))
finally:
    connection.close()
    client_socket.close()