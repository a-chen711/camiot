from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from keras.preprocessing import image
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
from keras.models import Model
from joblib import load
import io
import socket
import struct
from PIL import Image
import numpy as np
import cv2
import sys
import pyautogui 
import time

# from videoClient import video_control
sys.path.insert(0,'Finger_Detection')
from crop import generate_crop
from finger_control import finger_control_f

import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import base64


onMsg = "1"
offMsg = "0"

#name:uclahciIP-lemurIP
applianceDict= {
    'Coffee maker' : ('192.168.0.249','192.168.1.7'),
    'TV' : ('192.168.0.101','192.168.1.63'),
    'Printer' : ('192.168.0.148','192.168.1.64'),
    'Minotor' : ('192.168.0.162','192.168.1.61'),
    'Door' : ('192.168.0.134','192.168.1.62'),
    'Lamp' : ('192.168.0.206','192.168.1.59'),
}

def callAppliace(appliaceName,ipAddr):
    print(appliaceName,"is selected")
    appliaceClient=socket.socket()
    appliaceClient.connect((ipAddr,80))
    time.sleep(1)
    return appliaceClient

def controlAppliance(appliaceClient, delay = 0.5):
    appliaceClient.send(onMsg.encode())
    time.sleep(delay)
    appliaceClient.send(offMsg.encode())
    time.sleep(delay)
    appliaceClient.send(onMsg.encode())
    time.sleep(delay)
    appliaceClient.send(offMsg.encode())
    appliaceClient.close()

def video_control(dec):
    print(pyautogui.size()) 
    print(pyautogui.position()) 
    print(dec)
    if dec =='':
        return
    if dec == 'Middle':
        pyautogui.press('space')
    elif dec == 'Left':
        pyautogui.hotkey("ctrlleft", "p")
    elif dec == 'Right':
        pyautogui.hotkey("ctrlleft", "n")
    else:
        pyautogui.press('esc')

def monitor_control(dec):
    if dec =='':
        return
    if dec == 'Down':
        img = np.zeros([3840,2160,3],dtype=np.uint8)
        img.fill(0)
        cv2.imshow('image',img)
        # cv2.waitKey(0)
        # pyautogui.press('space')
    else:
        pyautogui.press('space')
        cv2.destroyAllWindows()

def printer_control(dec):
    pyautogui.hotkey("ctrlleft", "p")
    if dec == 'Down':
        print('Manually print.')
    elif dec == 'Middle':
        print('Print on the default setting.')
        pyautogui.press('enter')
    elif dec == 'Right':
        print('Printer right. Double print.')
        pyautogui.click(609, 845) 
        pyautogui.click(677, 432) 
    elif dec == 'Left':
        print('Printer left.')

def door_control(dec):
    global applianceDict
    if dec == 'Down':
        print('Door closed.')
        # make if blink twice
        DoorTuple=applianceDict['Door']
        applianceClient=callAppliace('Door',DoorTuple[1])
        controlAppliance(applianceClient)
    else:
        print('Door Open.')
        # make if blink twice with a longer interval
        DoorTuple=applianceDict['Door']
        applianceClient=callAppliace('Door',DoorTuple[1])
        controlAppliance(applianceClient)

def coffee_control(dec):
    if dec == 'Down':
        print('Coffee maker off.')
    else:
        print('The coffee is 60% full.')

def lamp_control(dec):
    if dec == 'Down':
        print('Lamp off.')
    else:
        print('Lamp on.')

    '''
    userInput = input("To turn ON press 1 or press 0 to turn OFF ... \n")
    userInput=int(userInput)
    if (userInput == 1):
        appliaceClient.send(onMsg.encode())
        appliaceClient.close()
    elif (userInput == 0):
        appliaceClient.send(offMsg.encode())
        appliaceClient.close()
    '''



channel = input('Channel:')
# control_scheme = input('Which control:(1-video,2-mouse,3-slides)')
control_scheme = '1'

# ------------------------------------------ #
#           Server Client Interface          #
# ------------------------------------------ #
# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
# server_socket.bind(('192.168.1.56', int(channel)))
server_socket.bind(('192.168.1.36', int(channel)))
server_socket.listen(0)
# counter = 0
# Accept a single connection and make a file-like object out of it
connection,add0 = server_socket.accept()
control = False

########################
time.sleep(2)
tServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#tServer.settimeout(0)
# tServer.bind(('192.168.1.56', int(channel)+10))
tServer.bind(('192.168.1.36', int(channel)+10))
# tServer.setblocking(0)
tServer.listen(0)
connect,addr = tServer.accept()
# tServer.setblocking(0)
#data=connect.recv(1024)
#print(data.decode("utf-8"))

#######################
layer = 'fc2'
base_model = VGG16(weights='imagenet')
model = Model(inputs=base_model.input, outputs=base_model.get_layer(layer).output)
clf = load('Finger_Detection/zomlp_classifier_Demo_Pi_Aug.joblib') 

counter = 0
control = False
obj = ''
control_signal = ''
# flag_f1 = True
flag_f1 = False
x_f1 = 0
x_f2 = 0
y_f1 = 0
y_f2 = 0

try:
    while True:
        time_in = time.time()
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        
        image_len = b''
        
        while True:

            image_frag = connection.recv(8192)
            #print(image_frag)
            if not image_frag:
                break
            image_len+=image_frag
        
        print(image_len)
        
        
        #image_len = connection.recv(65534)
        print(len(image_len))
        if not image_len:
            break
        # Construct a stream to hold the image data and read the image
        # data from the connection
        
        print('pic input time',time.time() - time_in)
        time_in = time.time()

        #img = generate_crop(file_path,240)
        info=connect.recv(1024)
        info = info.decode()
        print('Get control signal:',info)
        if info == 'Rec':
            cv2.destroyAllWindows()
            control = False
            flag_f1 = False
            # 180,135
            x_f1 = 60
            x_f2 = 0
            y_f1 = 20
            y_f2 = 0
            direc = str(counter)+'imageRec.jpg'
        elif info == 'Con':
            control = True
            direc = str(counter)+'imageCon.jpg'
        else:
            direc = str(counter)+'image.jpg'

        with open(direc, "wb") as fh:
            fh.write(base64.decodebytes(image_len))
        counter += 1


        if not control:
            # reset directions
            print('Doing classification.')
            test_set = []
            img_crop,img_bk = generate_crop(direc,220)

            img_bk,k,top,mid,control_signal = finger_control_f(direc,200, 5,-70,3)
            x_f1 = mid
            y_f1 = top
            cv2.imshow('Binary Image', img_bk)
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

                #print(predict_target)
                applianceTuple=applianceDict[predict_target]
                indexCount = 0
                cur_time = time.time()
                prev_time = time.time()
                while True:
                    # print('in the loop')
                    # print(indexCount)
                    print("orderedList ",clf.classes_[orderedIndex[indexCount]])
                    # applianceClient=callAppliace(clf.classes_[orderedIndex[indexCount]],applianceTuple[1])
                    # controlAppliance(applianceClient)

                    info=connect.recv(1024)
                    info = info.decode()
                    if info == 'ACK':
                        print(info)
                        obj = clf.classes_[orderedIndex[indexCount]]
                        break
                    elif info == '':
                        print('Interrupted.')
                        break
                    indexCount += 1
                    if indexCount > 5:
                        indexCount = 0
                    #prev_time = time.time()
                    #   break
                    # except:
                        # info = ''

                        #applianceClient=callAppliace(predict_target,applianceTuple[1])
                        #controlAppliance(applianceClient)
                #print('probability.')
                #print(clf.classes_)
                #print(predict_prob)
            # control = True

        else :
            # dir_f1 = dir_f2
            img_bk,k,top,mid,control_signal = finger_control_f(direc,200, 5,-70,3)
            height,width = img_bk.shape
            if flag_f1:
                if top > height - 30:
                    pyautogui.press('l')
                    continue
                else:
                    pyautogui.press('r')
                    x_f1 = mid
                    y_f1 = top
            x_f2 = mid
            y_f2 = top
            print('slope is ',k,'top y value is ',top,' and mid value is ', mid)
            print('control signal is', control_signal)
            
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

            print('done finger detection',time.time() - time_in)
            time_in = time.time()
            # quite
            if control_signal == 'Down':
                pyautogui.press('enter')
                connect.sendall(b'Stop Con.')
                continue
                # print('go down')
                # pyautogui.press('down')
                # time.sleep(0.4)
                # connect.sendall(b'Doing Con.')

            else:
                # print('control object is',obj)
                # height,width = img_bk.shape
                connect.sendall(b'No stop Con.')
                slope = height/width
                if (control_scheme=='1'):
                    # Control Part - video
                    xx_thres = 10
                    yy_thres = 10
                    # y axis
                    delta_y_f = y_f2 - y_f1
                    delta_x_f = x_f2 - x_f1
                    
                    steps_y = delta_y_f / 10
                    steps_x = delta_x_f / 10
                    
                    # if steps_x < 0:
                    #   for x_type in range(abs(int(steps_x))):
                    #       pyautogui.press('left')
                    # elif steps_x > 0:
                    #   for x_type in range(abs(int(steps_x))):
                    #       pyautogui.press('right')
                    
                    # if steps_y < 0:
                    #   for y_type in range(abs(int(steps_y))):
                    #       pyautogui.press('up')
                    # elif steps_y > 0:
                    #   for y_type in range(abs(int(steps_y))):
                    #       pyautogui.press('down')
                    # pyautogui.press('enter')


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
                        
                    # else:
                    #   print('y stay')
                    #   # x axis
                    #   delta_x_f = x_f2 - x_f1
                    #   if delta_x_f > xx_thres:
                    #       print('go right')
                    #       pyautogui.press('right')
                    #   elif delta_x_f < -xx_thres:
                    #       print('go left')
                    #       pyautogui.press('left')
                    #   else:
                    #       print('x stay')
                elif (control_scheme=='2'):
                    # Control Part - video 
                    if flag_f1:
                        x0, y0 = pyautogui.size()
                        pyautogui.moveTo(x0/2,y0/2)
                    delta_y_f = (y_f2 - y_f1)*5
                    delta_x_f = (x_f2 - x_f1)*5
                    pyautogui.moveTo(delta_x_f+x0/2, delta_y_f+y0/2)
                elif (control_scheme=='3'):
                    # Control Part - slides 
                    # y axis
                    delta_y_f = y_f2 - y_f1
                    if delta_y_f > 15:
                        print('go down')
                        pyautogui.press('down')
                    elif delta_y_f < -15:
                        print('go up')
                        pyautogui.press('up')
                else:
                    print('no control')
                    control_scheme = input('Which control:(1-video,2-mouse,3-slides)')
                    connect.sendall(b'Stop Con.')
                    continue

                # ack it is done
                time.sleep(0.7)
                connect.sendall(b'Doing Con.')

                # show the threshold line
                # for pix_i in range(height-1):
                #   img_bk[pix_i, min(x_f1+xx_thres,width-1)] = 127
                #   img_bk[pix_i, max(x_f1-xx_thres,0)] = 127
                # for pix_j in range(width-1):
                #   img_bk[max(y_f1-yy_thres,0),pix_j] = 127
                #   img_bk[min(y_f1+yy_thres,height-1),pix_j] = 127
            
            # disable flag
            flag_f1 = False

            cv2.imshow('Binary Image', img_bk)
            cv2.waitKey(5)


            
finally:
    connection.close()
    server_socket.close()
