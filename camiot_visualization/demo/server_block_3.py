from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# ------------------------------------------ Import models & files  ------------------------------------------ #
#mqtt modules
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
#PIL for pillow used to crop image and whatnot;
from PIL import Image
import base64
import time
#VGG16 Neural Network modules
from keras.preprocessing import image
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
from keras.models import Model
from joblib import load
from PIL import Image
import numpy as np
import cv2
import sys
import pyautogui
import socket

sys.path.insert(0,'Finger_Detection') #A list of strings that specifies the search path for modules
from crop import generate_crop
from finger_control_old import finger_control_f

# ------------------------------------------ SOCKET Functions  ------------------------------------------ #

strbroker = "192.168.1.26" #NOT SURE WHAT THIS IS?
tServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#socket.AF_INET = address and protocol families (IPv4)
#socket.SOCK_STREAM = socket type (TCP)
##BOTH OF THESE ARE CONSTANTS
#This serves to create the socket. 
tServer.bind(('192.168.1.25', 8000)) #laptop ip address
tServer.listen(0)
connect,addr = tServer.accept()

step_size = 20
binary_thre = 180
size = np.pi/4 #used to be pi/6 but perhaps pi/4 is a better 
brightness_thre = 50

# ------------------------------------------ MQTT Functions  ------------------------------------------ #

#MQTT is always between client and broker
#client sends a connect message to the broker and the broker responds with a CONNACK message and status back
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("image")

#once the connection is established, broker keeps connection opne until a disconnect commnand is sent.
#callback for when publish message is received from the server
def on_message(client, userdata, msg):
    global obj, command_in, down_confirm,x_ref,y_ref, k_ref, mid_ref
    
    
    if msg.topic == 'image': 
        t1 = time.time()
        print("message received time = " + str(t1))
        with open('1.png', "wb") as fh:
            fh.write(base64.decodebytes(msg.payload))
        info=connect.recv(1024)
        info = info.decode()
        print('Get control signal:',info)
        
        #doesn't matter from here
        if info == 'rec':
            command_in = False
            down_confirm = False
            x_ref = None
            y_ref = None
            k_ref = None

            print('Doing classification.')
            test_set = []
            img_crop,img_bk = generate_crop('1.png',220)
            #
            img_bk,k,top,mid,control_signal,x_mid = finger_control_f('1.png',binary_thre, 5,-70,3)
            
            #cv2.imshow('Binary Image', img_bk)
            cv2.waitKey(3)
            
            cv2.imwrite('2nd_step.jpg',img_crop)
        
            img = image.load_img('2nd_step.jpg', target_size=(224, 224))
            img_data = image.img_to_array(img)
            img_data = np.expand_dims(img_data, axis=0)
            img_data = preprocess_input(img_data)
            
            vgg16_feature = model.predict(img_data)
            test_set.append(np.ndarray.tolist(vgg16_feature[0]))
            #print(test_set)

            if test_set:
                predict_target = clf.predict(test_set)
                print(predict_target.shape)
                print(predict_target.size)
                predict_prob = clf.predict_proba(test_set)
                #print(correct_tag)
                print('predict results.')
                print(clf.classes_)
                print(predict_prob)
                prob = predict_prob[0]
                orderedIndex=sorted(range(len(prob)), key=lambda k: prob[k], reverse=True)
                print(orderedIndex)
                print("appliances in order")
                validNum = 0
                validNum = len([i for i in prob if i > 0.075]) - 1
                print('There are valid object #', validNum)
                # get all the results in order and loop thru
                print(predict_target)
                predict_target=predict_target[0]
                
                for indexCount in orderedIndex:
                    print(clf.classes_[indexCount],end=" ")
                
                
                indexCount = 0
                
                while True:
                    print("orderedList ",clf.classes_[orderedIndex[indexCount]])
                    info_2=connect.recv(1024)
                    info_2 = info_2.decode()
                    if info_2 == 'ACK':
                        print(info_2)
                        obj = clf.classes_[orderedIndex[indexCount]]
                        break
                    elif info_2 == '':
                        print('Interrupted.')
                        break
                    indexCount += 1
                    if indexCount > 5:
                        indexCount = 0
                connect.sendall(b'ready')
                time.sleep(0.5)
                connect.sendall(b'Doing Con.')

        #don't care up until here 
        elif info == 'con':
            t2 = time.time()
            #print(obj)
            #print('Con coming soon.')
            
            #img_bk is just image itself
            #top,mid is the coord of fingertip
            #xmid is the intercept that slope makes with frame
            img_bk,k,top,mid,control_signal,x_mid = finger_control_f('1.png',binary_thre, 5,-70,3)
            
            cv2.imwrite('../binary.png',img_bk)
            height,width = img_bk.shape
            t3 = time.time()
            #print(top,mid)

            #print(k,x_mid)
            if obj == 'Printer':
                pyautogui.press('a')
            elif obj =='Coffee maker':
                pyautogui.press('b')
            elif obj =='TV':
                pyautogui.press('c')
            elif obj =='Door':
                pyautogui.press('d')
            elif obj =='Minotor':
                pyautogui.press('e')

            #print('slope is ',k,'top y value is ',top,' and mid value is ', mid)
            #print('control signal is', control_signal)
            ##############################
            #creating reference photo and compares future images to reference image
            if not x_ref or not y_ref or not k_ref:
                x_ref = mid
                y_ref = top
                mid_ref = x_mid
                if mid == x_mid:
                    direction = np.pi/2 - 0.01
                #print(top/(mid-x_mid))
                else:
                    direction=np.arctan(top/float((mid-x_mid)))
                k_ref = direction
                connect.sendall(b'Doing Con.')
            else:
            	#if no finger, then sends a "down" flag 
                # quite
                if control_signal == 'Down':
                    print('down')
                    pyautogui.press('m')
                    if command_in:
                        down_confirm = True
                    time.sleep(0.01)
                    connect.sendall(b'Doing Con.')
                    #print(down_confirm)


                #####        
                else:
                    command_in = True
                    print('up')
                    pyautogui.press('n')

                    if mid == x_mid:
                        direction = k_ref
                    #print(top/(mid-x_mid))
                    else:
                        direction=np.arctan(top/float((mid-x_mid)))
                    print(direction - k_ref)
                    print(x_mid - mid_ref)

                    #mid_ref is xmid of the reference image
                    #k_ref = direction is the slope
                    #"//5" returns the integer digit of the width / 5
                    #if xmid coord - midref bigger than width /5
                    #width is 224 for this 
                    #maybe don't include the midref calculations? Moving xmid does not necessarily mean they are pointing at that box 
                    if (x_mid - mid_ref > width//5) or (direction - k_ref > size):
                        print('block 4')
                        block = 8
                        pyautogui.press('8')
                    elif (x_mid - mid_ref < -width // 5) or (direction - k_ref < -size):
                        print('block 1')
                        block = 2
                        pyautogui.press('2')
                    elif (direction - k_ref < size) :
                        print('block 2')
                        block = 4
                        pyautogui.press('4')
                    elif (direction - k_ref > -size):
                        print('block 3')
                        block = 6
                        pyautogui.press('6')
                #### revise this part
                #trying to integrate using the slope of finger and finger mid to indicate block correctly
                #direction is angle from xmid to top,mid
                #quadrant 4 is actually left side 
                #size is alpha from the diagram 
                #add time.sleep(time) only to server 


                    if down_confirm == True:
                        down_confirm = False
                        command_in = False
                        #connect.sendall(b'Stop Con.')
                        connect.sendall(b'Doing Con.')
                    else:
                        connect.sendall(b'Doing Con.')
        
                


layer = 'fc2'
base_model = VGG16(weights='imagenet')
model = Model(inputs=base_model.input, outputs=base_model.get_layer(layer).output)
clf = load('Finger_Detection/zomlp_classifier_Demo_Pi_Aug.joblib') 

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message


client.connect(strbroker, 1883, 60)
client.loop_forever()
            