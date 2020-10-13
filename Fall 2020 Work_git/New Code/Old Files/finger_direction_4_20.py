import cv2
import numpy as np
import os.path as osp
from skimage.measure import label
from cv2 import Canny

NO_FIGURE_PIXEL_NUM_THRESHOLD = 1000
GRADIENT_LINE_LENGTH_FOR_VIS = 50

finger_flag=True

#INPUT_PATH = '/Users/ApplePro/Desktop/School/GradSchool/Research /HCI/camiot/Feb 15/Yuan /FI_evaluationSet/tv/extras'


def finger_recognition(item):
    if '.jpg' not in item and '.png' not in item:
        print('not a valid image')
    else:
        image = cv2.imread(item)
        imageYCrCb = cv2.cvtColor(image, cv2.COLOR_BGR2YCR_CB)

        # skin detection
        min_YCrCb = np.array([0, 133, 77], np.uint8)
        max_YCrCb = np.array([255, 173, 127], np.uint8)
        skinRegionYCrCb = cv2.inRange(imageYCrCb, min_YCrCb, max_YCrCb)

        # cv2.imwrite(osp.join(OUTPUT_PATH, '{}_{}_debug_mask.jpg'.format(item.split('.')[0], 'skin')), cv2.bitwise_and(image, image, mask=np.uint8(skinRegionYCrCb)))

        # preprocessing
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
        skinRegionYCrCb = cv2.erode(skinRegionYCrCb, kernel, iterations=2)
        skinRegionYCrCb = cv2.dilate(skinRegionYCrCb, kernel, iterations=2)
        skinRegionYCrCb = cv2.GaussianBlur(skinRegionYCrCb, (3, 3), 0)

        # cv2.imwrite(osp.join(OUTPUT_PATH, '{}_{}_debug_mask_after_processing.jpg'.format(item.split('.')[0], 'skin')), cv2.bitwise_and(image, image, mask=np.uint8(skinRegionYCrCb)))

        # another filter
        image = image.astype('uint8')
        image_canny_filter = Canny(image=image, threshold1=20, threshold2=40)
        image_canny_filter = (image_canny_filter < 100).astype(np.int32)
        # cv2.imwrite(osp.join(OUTPUT_PATH, '{}_{}_canny_as_filter.jpg'.format(item.split('.')[0], 'skin')), image_canny_filter*255)
        image_canny_filter_left = np.roll(image_canny_filter, 1, axis=0)
        image_canny_filter_right = np.roll(image_canny_filter, -1, axis=0)
        image_canny_filter_up = np.roll(image_canny_filter, 1, axis=1)
        image_canny_filter_down = np.roll(image_canny_filter, -1, axis=1)
        image_sobel = skinRegionYCrCb * image_canny_filter * image_canny_filter_left * image_canny_filter_right * image_canny_filter_up * image_canny_filter_down

        # largest island
        #image_sobel = label(image_sobel)
        #image_sobel = image_sobel == np.argmax(np.bincount(image_sobel.flat)[1:]) + 1
        image_sobel = label(image_sobel)
        image_sobel_copy = image_sobel.copy()
        sorted_bin_indexes = np.bincount(image_sobel_copy.flat)[1:].argsort()[::-1]
        found_flag = 0
        for i in range(len(sorted_bin_indexes)):
            image_sobel = image_sobel_copy == sorted_bin_indexes[i] + 1
            points_x, points_y = np.where(image_sobel == 1)
            top_line_index = np.min(points_x)
            bot_line_index = np.max(points_x)
            if bot_line_index >= 0.9 * image_sobel.shape[0] and top_line_index >= 0.2 * image_sobel.shape[0]:
                found_flag = 1
                break
        if found_flag == 0:
            print('no finger detected.{}'.format(item))
            finger_flag=False 
            return finger_flag,0
            #return None

        # cv2.imwrite(osp.join(OUTPUT_PATH, '{}_{}_canny_as_filter.jpg'.format(item.split('.')[0], 'skin')), image_canny_filter)

        # postprocessing
        image_sobel = image_sobel.astype(np.uint8)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4))
        image_sobel = cv2.dilate(image_sobel, kernel, iterations=2)
        image_sobel = cv2.GaussianBlur(image_sobel, (3, 3), 0)
        image_sobel = image_sobel.astype(np.int32)
        if np.count_nonzero(image_sobel) <= NO_FIGURE_PIXEL_NUM_THRESHOLD:
            print('no finger detected.{}'.format(item))
            finger_flag=False 
            return finger_flag,0
            #return None

        # get directions
        # get mid points
        image_sobel_copy = np.zeros_like(image_sobel)
        points_x, points_y = np.where(image_sobel == 1)
        top_line_index = np.max(points_x)
        bot_line_index = np.min(points_x)
        mid_line_index = (top_line_index + bot_line_index) // 2
        line_length = top_line_index - bot_line_index + 1 - 6
        top_line_index = mid_line_index - line_length // 2
        bot_line_index = mid_line_index + line_length // 2
        mid_points = []
        for i in range(top_line_index, bot_line_index+1):
            y_coordinates = np.where(image_sobel[i, :] == 1)
            mid_points.append((i, np.mean(y_coordinates).astype(np.int32)))
        #     cv2.circle(image_sobel_copy, (np.mean(y_coordinates).astype(np.int32), i), 8, 255, 2)
        # cv2.imwrite(osp.join(OUTPUT_PATH, '{}_{}_mid_points.jpg'.format(item.split('.')[0], 'skin')), image_sobel_copy)
        # cv2.circle(image_sobel, (int(np.mean([item[1] for item in mid_points])), int(np.mean([item[0] for item in mid_points]))), 8, 2, 2)
        # cv2.imwrite(osp.join(OUTPUT_PATH, '{}_{}_average_mid_points.jpg'.format(item.split('.')[0], 'skin')), image_sobel * 100)

        mid_gradients = []
        # get gradient
        for i in range(0, line_length // 2):
            mid_gradients.append(
                np.arcsin(
                    (mid_points[i+line_length//2+1][1] - mid_points[i][1]).astype(np.float32)
                    /
                    np.math.sqrt(np.math.pow((mid_points[i+line_length//2+1][1]-mid_points[i][1]+1).astype(np.float32), 2.0)+np.math.pow(line_length//2+2, 2.0))
                ) / np.pi * 180.0
            )
        if len(mid_gradients) == 0:
            print('no finger detected.')
            finger_flag=False 
            return finger_flag,0
            #return None
        average_mid_gradient = np.mean(mid_gradients)
        start_point = (int(np.mean([item[1] for item in mid_points])), int(np.mean([item[0] for item in mid_points])))
        end_point = (int(start_point[0]+GRADIENT_LINE_LENGTH_FOR_VIS * np.sin(average_mid_gradient * np.pi / 180.0)), int(start_point[1]+GRADIENT_LINE_LENGTH_FOR_VIS * np.cos(average_mid_gradient * np.pi / 180.0)))
        #cv2.line(image_sobel, start_point, end_point, 2, 2)
        #cv2.imwrite(osp.join(OUTPUT_PATH, '{}_seg_and_gradient_{}.jpg'.format(item.split('.')[0], average_mid_gradient)), image_sobel * 100)
        finger_flag=True
        return finger_flag,average_mid_gradient



#mid=finger_recognition('/Users/ApplePro/Desktop/School/GradSchool/Research /HCI/camiot/Feb 15/Yuan /FI_evaluationSet/tv/extras/71.jpg')
#print(mid)











