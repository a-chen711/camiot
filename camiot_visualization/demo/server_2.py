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

strbroker = "192.168.1.22"
tServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tServer.bind(('192.168.1.18', 8000))
tServer.listen(0)
connect,addr = tServer.accept()

step_size = 20
binary_thre = 200

# ------------------------------------------ MQTT Functions  ------------------------------------------ #
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("image")

def on_message(client, userdata, msg):
    global obj, x_f1, y_f1
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
            x_f1,y_f1 = None, None
            print('Doing classification.')
            test_set = []
            img_crop,img_bk = generate_crop('1.png',220)

            img_bk,k,top,mid,control_signal = finger_control_f('1.png',200, 5,-70,3)
            x_f1 = mid
            y_f1 = top
            #cv2.imshow('Binary Image', img_bk)
            cv2.waitKey(5)
            
            cv2.imwrite('2nd_step.jpg',img_crop)
        
            img = image.load_img('2nd_step.jpg', target_size=(224, 224))
            img_data = image.img_to_array(img)
            img_data = np.expand_dims(img_data, axis=0)
            img_data = preprocess_input(img_data)
            

            vgg16_feature = model.predict(img_data)
            test_set.append(np.ndarray.tolist(vgg16_feature[0]))

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
            
            img_bk,k,top,mid,control_signal = finger_control_f('1.png',binary_thre, 5,-70,3)
            height,width = img_bk.shape
            t3 = time.time()
            print(top,mid)

            
            if not x_f1 or not y_f1:
                #too high
                if height - top < height/4: 
                    pyautogui.press('i')
                #too low
                elif height - top > height*3/4:
                    pyautogui.press('k')
                #left
                elif width - mid < width/4:
                    pyautogui.press('j')
                #right
                elif width - mid > width*3/4:
                    pyautogui.press('l')
                else:
                    #great
                    x_f1 = mid
                    y_f1 = top
                    pyautogui.press('r')
                    time.sleep(1)
            else:

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

                x_f2 = mid
                y_f2 = top
                #print('slope is ',k,'top y value is ',top,' and mid value is ', mid)
                print('control signal is', control_signal)
                print(x_f2-x_f1,y_f2-y_f1)
                    

                #print('done finger detection',time.time() - time_in)
                time_in = time.time()
                # quite
                if control_signal == 'Down':
                    pyautogui.press('enter')
                    #connect.sendall(b'Stop Con.')
                    t4 = time.time()
                    connect.sendall(b'Doing Con.')

                else:
                    slope = height/width
                    xx_thres = 20
                    yy_thres = 15
                    # y axis
                    delta_y_f = y_f2 - y_f1
                    delta_x_f = x_f2 - x_f1
                    
                    steps_y = delta_y_f / step_size
                    steps_x = delta_x_f / step_size
                    
                    #print(steps_x,steps_y)
                    if steps_x < 0:
                        for x_type in range(abs(int(steps_x))):
                            pyautogui.press('z') # left
                    elif steps_x > 0:
                        for x_type in range(abs(int(steps_x))):
                            pyautogui.press('x') #right
                    
                    if steps_y < 0:
                        for y_type in range(abs(int(steps_y))):
                            pyautogui.press('n') #up
                    elif steps_y > 0:
                        for y_type in range(abs(int(steps_y))):
                            pyautogui.press('m') #down
                    else:
                        pyautogui.press('p') #middle

                    pyautogui.press('enter')


                    if (delta_x_f > xx_thres or delta_x_f < -xx_thres) or (delta_y_f > yy_thres or delta_y_f < -yy_thres):
                        # left
                        if delta_y_f < -slope * delta_x_f and delta_y_f > slope * delta_x_f:
                            print('go left')
                            pyautogui.press('left') 
                        # right
                        elif delta_y_f > -slope * delta_x_f and delta_y_f < slope * delta_x_f:
                            print('go right')
                            pyautogui.press('right')
                        elif delta_y_f > -slope * delta_x_f and delta_y_f > slope * delta_x_f:
                            print('go down')
                            pyautogui.press('down')
                        elif delta_y_f < -slope * delta_x_f and delta_y_f < slope * delta_x_f:
                            print('go up')
                            pyautogui.press('up')
                    else:
                        print('STAY.')
                        pyautogui.press('v') 
                    time.sleep(0.05)
                    t4 = time.time()
                    connect.sendall(b'Doing Con.')
                t5 = time.time()
                #print(t2-t1,t3-t2,t4-t3,t5-t4)


layer = 'fc2'
base_model = VGG16(weights='imagenet')
model = Model(inputs=base_model.input, outputs=base_model.get_layer(layer).output)
clf = load('Finger_Detection/zomlp_classifier_Demo_Pi_Aug.joblib') 

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message


client.connect(strbroker, 1883, 60)
client.loop_forever()
            
