from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# ------------------------------------------ Import models & files  ------------------------------------------ #
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from PIL import Image
import base64
import time
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

sys.path.insert(0,'Finger_Detection')
from crop import generate_crop
from finger_control import finger_control_f

strbroker = "192.168.1.26"
tServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tServer.bind(('192.168.1.25', 8000))
tServer.listen(0)
connect,addr = tServer.accept()

step_size = 20
binary_thre = 190
size = np.pi/18

# ------------------------------------------ MQTT Functions  ------------------------------------------ #
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("image")

def on_message(client, userdata, msg):
    global obj, command_in, down_confirm
    
    
    #print(msg.topic)
    if msg.topic == 'image': 

        #print(len(msg.payload))
        #print('image transmitted')
        t1 = time.time()
        with open('1.png', "wb") as fh:
            fh.write(base64.decodebytes(msg.payload))
        info=connect.recv(1024)
        info = info.decode()
        print('Get control signal:',info)

        if info == 'rec':
            command_in = False
            down_confirm = False

            print('Doing classification.')
            test_set = []
            img_crop,img_bk = generate_crop('1.png',220)

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


        elif info == 'con':
            t2 = time.time()
            #print(obj)
            #print('Con coming soon.')
            
            img_bk,k,top,mid,control_signal,x_mid = finger_control_f('1.png',binary_thre, 5,-70,3)
            cv2.imwrite('../binary.png',img_bk)
            height,width = img_bk.shape
            t3 = time.time()
            #print(top,mid)

            print(k,x_mid)
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
            
            t4 = time.time()
            # quite
            if control_signal == 'Down':
                print('down')
                pyautogui.press('m')
                if command_in:
                    down_confirm = True
                time.sleep(0.01)
                connect.sendall(b'Doing Con.')
                #print(down_confirm)
                    
            else:
                command_in = True
                print('up')
                pyautogui.press('n')
                if mid == x_mid:
                    direction = np.pi/2 - 0.01
                #print(top/(mid-x_mid))
                else:
                    direction=np.arctan(top/float((mid-x_mid)))
                print(direction)
                if (x_mid > width*3.2//4):
                    print('block 4')
                    block = 8
                    pyautogui.press('8')
                elif x_mid > width*1.15//2 and x_mid < width*3.1//4:
                    print('block 3')
                    block = 6
                    pyautogui.press('6')
                elif x_mid < width*1.05// 2 and x_mid > width *7//20 :
                    print('block 2')
                    block = 4
                    pyautogui.press('4')
                elif x_mid < width*6.9//20:
                    print('block 1')
                    block = 2
                    pyautogui.press('2')
                '''
                if direction > 0 and direction < np.pi/2 - size:
                    print('block 4')
                    block = 8
                    pyautogui.press('8')
                elif direction > np.pi/2 - size and direction < np.pi/2:
                    print('block 3')
                    block = 6
                    pyautogui.press('6')
                elif direction < 0 and direction > - np.pi/2 + size:
                    print('block 1')
                    block = 2
                    pyautogui.press('2')
                elif direction < -np.pi/2 + size:
                    print('block 2')
                    block = 4
                    pyautogui.press('4')
                '''
                #print('here')
                #print(down_confirm)
                if down_confirm == True:
                    down_confirm = False
                    command_in = False
                    #connect.sendall(b'Stop Con.')
                    connect.sendall(b'Doing Con.')
                else:
                    connect.sendall(b'Doing Con.')
            t5 = time.time()
            print(t2-t1,t3-t2,t4-t3,t5-t4)


layer = 'fc2'
base_model = VGG16(weights='imagenet')
model = Model(inputs=base_model.input, outputs=base_model.get_layer(layer).output)
clf = load('Finger_Detection/zomlp_classifier_Demo_Pi_Aug.joblib') 

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message


client.connect(strbroker, 1883, 60)
client.loop_forever()
            
