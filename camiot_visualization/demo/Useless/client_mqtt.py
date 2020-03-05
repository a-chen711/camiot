import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import time
import time
import picamera
from gpiozero import Button
import sys
import base64
from imuTri import trigger

from testImuConNew import imuTri

strbroker = "192.168.1.5"
server_ip = '192.168.1.36'
info  = 'not entered'
ack_info = ''
feedback_info = ''
'''
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe("feedback")
    

def on_message(client, userdata, msg):
    if msg.topic == 'feedback':
        feedback_info = msg.payload.decode('utf-8')

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(server_ip, 1883, 60)
'''
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
        
        print('To take picture twist your wrist twice and point at your object')
        
        imuTri()
        time.sleep(0.2)
        print('taking photos...\n')
        info = 'rec'
        publish.single("command/rec", info ,hostname = strbroker)
        camera.color_effects = None
        camera.resolution = (224,224)
        for num in range(1):
            camera.capture('1.png')
            # Write the length of the capture to the stream and flush to
            # ensure it actually gets sent
            with open("1.png", "rb") as img_file:
                my_string = base64.b64encode(img_file.read())
                print(len(my_string)) 
            publish.single("image", my_string ,hostname = strbroker)
            time.sleep(0.1)
        print('Done!')
        
        print('move to the selection part.')
        select=0
        info_counter = -15
        
        while True:
            if trigger(1.5) == False:
                print('selecting')
                ack_info = 'ACK'
                publish.single("confirm_img", ack_info ,hostname = strbroker)
                break
            else:
                print('changing')
                ack_info = 'NI'
                publish.single("confirm_img", ack_info ,hostname = strbroker)
                time.sleep(0.5)
       
        print("Done!")
        print("taking photo for finger control place your finger in position")
        time.sleep(0.6)
        print('recording...')
        # info = 'Con'
        # tSocket.sendall(info.encode('utf-8'))
        camera.color_effects = (128,128)
        camera.resolution = (224,224)

        info = 'con'
        publish.single("command/con", info ,hostname = strbroker)
        for num in range(80):
            
            camera.capture('2.png')
            with open("2.png", "rb") as img_file:
                my_string = base64.b64encode(img_file.read())
            publish.single("image", my_string ,hostname = strbroker)
        print('Con part coming soon.')
finally:
    camera.close()
    print('Done')