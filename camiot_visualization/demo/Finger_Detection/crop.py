import numpy as np
import cv2 
from matplotlib import pyplot as plt
import os
from binary_image import binary_image_r

def generate_crop(img_dir,thre):
    img_o = cv2.imread(img_dir)
    img = binary_image_r(img_o,thre)
    
    #img = cv2.cvtColor(img_in.copy(),cv2.COLOR_BGR2GRAY)
    height,width = img.shape
    #print(width-9)
    all_ct_pt =[]
    slope = []


    white_areas=[]
    start_point = 8
    current_point = 8
    white_thr = 230
    black_thr = 10
    for pixel in range(4,width-4,4):
        #print((pixel,img[height-1,pixel]))
        if img[height-1,pixel] >white_thr:
            if img[height-1, pixel - 4] < black_thr :
                start_point = pixel
            elif img[height-1, pixel - 4] >white_thr or img[height-1, pixel + 4] > white_thr:
                current_point = pixel
            if pixel > width -9:

                current_point = pixel
                if current_point - start_point >12:
                    white_areas.append((start_point,current_point))
        elif img[height-1,pixel] < black_thr:
            if img[height-1, pixel - 4] >white_thr and  current_point - start_point >12:

                white_areas.append((start_point,current_point))
    #print('White areas: ',white_areas)
    if white_areas ==[]:
        return img_o,img
    else:
        max_dif = 0
        for item in white_areas:
            if item[1] - item[0] > max_dif:
                max_dif = item[1] - item[0]
                mid_point = int(np.mean(item))
        
        #print(max_dif)
        if max_dif > width // 3:
            #print('Cropping!')
            img_o = img_o[:height*80//100,:]
            img = binary_image_r(img_o,thre)
    
            #img = cv2.cvtColor(img_in.copy(),cv2.COLOR_BGR2GRAY)
            height,width = img.shape
            all_ct_pt =[]
            slope = []


            white_areas=[]
            start_point = 8
            current_point = 8
            white_thr = 240
            black_thr = 10
            for pixel in range(4,width-4,4):
                #print((pixel,img[height-1,pixel]))
                if img[height-1,pixel] > white_thr:
                    if img[height-1, pixel - 4] < black_thr :
                        start_point = pixel
                    elif img[height-1, pixel - 4] >white_thr or img[height-1, pixel + 4] > white_thr:
                        current_point = pixel
                    elif pixel > width -9:
                        current_point = pixel
                        if current_point - start_point >12:
                            white_areas.append((start_point,current_point))
                elif img[height-1,pixel] == 0:
                    if img[height-1, pixel - 4] >white_thr and  current_point - start_point >12:
                        white_areas.append((start_point,current_point))

        if white_areas ==[]:
            
            return img_o,img
        else:
            cur_max = height
            choice = white_areas[0]
            for item in white_areas:
                cur_reach = height
                cur_mid = int(np.mean(item))
                for line in range(height-1,0,-4):
                    if img[line,cur_mid] < black_thr:
                        if line < cur_max:
                            choice = item
                            cur_max = line
                        break

        mid_point = int(np.mean(choice))
        bottom_mid = mid_point
        to_crop_v = height / 2
        to_crop_h = width / 2

        for line in range(height-1,0,-4):
            #print('Here we are')
            
            if img[line,mid_point] <10:
                
                if img[max(0,line-15),mid_point] <10 and img[max(0,line-30),mid_point] <10 and img[max(0,line-15),max(0,mid_point-15)] <10\
                 and img[max(0,line-15),min(width-1,mid_point+15)] <10 and img[max(0,line-30),min(width-1,mid_point+30)] <10:
                    to_crop_v = line
                    to_crop_width = int(line / float(398) * 532)
                    break
                else:
                    continue
                
            for pixel in range(mid_point,width):
                if img[line,pixel] <10 or pixel > width-9:
                    rt_most = (line,pixel)
                    break
            for pixel in range(mid_point,0,-1):
                if img[line,pixel] <10 or pixel < 9:
                    lf_most = (line,pixel)
                    break
            #print((lf_most,rt_most))
            mid_point = int(np.mean([lf_most[1],rt_most[1]]))

            #print(lf_most[1])
            #print(rt_most[1])
            if line == height-1:
                base_pt = (line,mid_point)
                all_ct_pt.append(base_pt)
            else:
                if img[line,mid_point] > 10:
                    ct_pt = (line,mid_point)
                    all_ct_pt.append(ct_pt)
                    if ct_pt[1] - base_pt[1] != 0:
                        slope.append(float(-(ct_pt[0] - base_pt[0]))/(ct_pt[1] - base_pt[1]))
                    else:
                        if not slope:
                            slope.append(float(-(ct_pt[0] - base_pt[0]))/1)
                        
                #print(ct_pt)
            #print(base_pt)
        #print(all_ct_pt)
        for item in all_ct_pt:
            img[item[0],item[1]] = 127
            img[item[0],item[1]+1] = 127
            img[item[0],item[1]-1] = 127
            img[item[0],item[1]+2] = 127
            img[item[0],item[1]-2] = 127

        #print((base_pt,ct_pt))
        #print(slope)
        general_k = np.median(slope[-5:])


        #print (slope)
        if general_k > 1.73 or general_k < -1.73 or np.isnan(general_k):
            direc = 'Middle'
        elif general_k < 1.73:
            direc = 'Middle'
        elif general_k > - 1.73 :
            direc = 'Left'

        print('General Direction of Finger is: %s with k value: %.2f' %(direc,general_k))



        desired_h_width = int(width * .6)
        #desired_h_width = to_crop_width
        y_value = height - to_crop_v
        #print(general_k)
        if np.isnan(general_k):
            x_value = 0
        else:
            x_value = int(y_value / general_k)

        if general_k > 0:
            critical_x_r = bottom_mid+x_value + int((1+1.0/general_k)/(2+1.0/general_k)*desired_h_width)
            critical_x_l = bottom_mid+x_value - int((1.0)/(2+1.0/general_k)*desired_h_width)
        elif general_k < 0:
            k_replace = abs(general_k)
            critical_x_r = bottom_mid+x_value + int((1.0)/(2+1.0/k_replace)*desired_h_width)
            critical_x_l = bottom_mid+x_value - int((1+1.0/k_replace)/(2+1.0/k_replace)*desired_h_width)

        else:
            critical_x_r = int(bottom_mid+x_value + desired_h_width//2)
            critical_x_l = int(bottom_mid+x_value - desired_h_width//2)
        #print(((bottom_mid+x_value) - max(0,critical_x_l),min(critical_x_r,width-1)-(bottom_mid+x_value)))
        #print((0,to_crop_v),(critical_x_l,critical_x_r))
        #print(img.shape)

        if to_crop_v < height * 2 //3:
            start_v = 0
        else:
            start_v = height * 20 //100
        img_cropped = img_o[start_v:to_crop_v,max(0,critical_x_l):min(critical_x_r,width-1)]
        #print(img.shape)
        for line in range(to_crop_v):
            img[line,max([0,critical_x_l])] = 150
            img_o[line,max([0,critical_x_l])] = [0,0,0]
        for line in range(to_crop_v):
            img[line,min(critical_x_r,width-1)] = 150
            img_o[line,min(critical_x_r,width-1)] = [0,0,0]
        for pixel in range(max([0,critical_x_l]),min([width-1,critical_x_r])):
            img[to_crop_v,pixel] = 150
            img_o[to_crop_v,pixel] = [0,0,0]

        #img_cropped = cv2.resize(img_cropped, (224,224), interpolation = cv2.INTER_AREA)
        #return img_cropped,img_o
        
    return img_cropped,img
if __name__ == "__main__":
    for file in os.listdir():

        filename = os.fsdecode(file)

        if filename.endswith(".jpg") and 'crp' not in filename and 'bk' not in filename: 
            img,img_bk = generate_crop(filename,220)
            cv2.imwrite(filename[:-4] + 'crp.jpg', img)
            cv2.imwrite(filename[:-4] + 'bk.jpg', img_bk)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

'''
cv2.imshow('Cropped Image',img_cropped)
cv2.imshow('Central Line',img)
cv2.imshow('Position in original image',img_o)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''