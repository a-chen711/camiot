import cv2
import numpy as np
import os.path as osp
from skimage.measure import label
import time
import os
import math

NO_FIGURE_PIXEL_NUM_THRESHOLD = 250
GRADIENT_LINE_LENGTH_FOR_VIS = 25

INPUT_PATH = '/home/pi/Camiot/finger_test_data_downsampled/'

def finger_recognition(image):
    # image_sobel_draw = np.zeros_like(image)
    imageYCrCb = cv2.cvtColor(image, cv2.COLOR_BGR2YCR_CB)

    # skin detection
    min_YCrCb = np.array([0, 133, 77], np.uint8)
    max_YCrCb = np.array([255, 173, 127], np.uint8)
    skinRegionYCrCb = cv2.inRange(imageYCrCb, min_YCrCb, max_YCrCb)

    # preprocessing
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    skinRegionYCrCb = cv2.erode(skinRegionYCrCb, kernel, iterations=1)
    skinRegionYCrCb = cv2.dilate(skinRegionYCrCb, kernel, iterations=1)
    skinRegionYCrCb = cv2.GaussianBlur(skinRegionYCrCb, (3, 3), 0)

    # another filter
    image = image.astype('uint8')
    image_canny_filter = cv2.Canny(image=image, threshold1=35, threshold2=70)
    image_canny_filter = (image_canny_filter < 150).astype(np.int32)

    image_canny_filter_left = np.roll(image_canny_filter, 1, axis=0)
    # image_canny_filter_right = np.roll(image_canny_filter, -1, axis=0)
    image_canny_filter_up = np.roll(image_canny_filter, 1, axis=1)
    # image_canny_filter_down = np.roll(image_canny_filter, -1, axis=1)
    # image_sobel = skinRegionYCrCb * image_canny_filter * image_canny_filter_left * image_canny_filter_right * image_canny_filter_up * image_canny_filter_down
    image_sobel = skinRegionYCrCb * image_canny_filter * image_canny_filter_left * image_canny_filter_up

    # largest island
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
        return None

    # postprocessing
    image_sobel = image_sobel.astype(np.uint8)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    image_sobel = cv2.dilate(image_sobel, kernel, iterations=2)
    image_sobel = cv2.GaussianBlur(image_sobel, (3, 3), 0)
    image_sobel = image_sobel.astype(np.int32)
    if np.count_nonzero(image_sobel) <= NO_FIGURE_PIXEL_NUM_THRESHOLD:
        print('no finger detected.{}'.format(item))
        return None

    # get directions
    # get mid points
    points_x, points_y = np.where(image_sobel == 1)
    top_line_index = np.max(points_x)
    bot_line_index = np.min(points_x)
    mid_line_index = (top_line_index + bot_line_index) // 2
    line_length = top_line_index - bot_line_index + 1 - 6
    top_line_index = mid_line_index - line_length // 2
    bot_line_index = mid_line_index + line_length // 2
    # mid_points = []
    mid_points_x =[]
    mid_points_y = []
    for i in range(top_line_index, bot_line_index+1):
        y_coordinates = np.where(image_sobel[i, :] == 1)
        # mid_points.append((i, np.mean(y_coordinates).astype(np.int32)))
        mid_points_x.append(i)
        mid_points_y.append(np.mean(y_coordinates).astype(np.int32))

    mid_points_x = np.array(mid_points_x)
    mid_points_y = np.array(mid_points_y)

    k = np.polyfit(mid_points_x, mid_points_y, 1)[0]
    theta = math.atan(k) / math.pi * 180

    # mid_gradients = []
    # # get gradient
    # for i in range(0, line_length // 2):
    #     mid_gradients.append(
    #         np.arcsin(
    #             (mid_points[i+line_length//2+1][1] - mid_points[i][1]).astype(np.float32)
    #             /
    #             np.math.sqrt(np.math.pow((mid_points[i+line_length//2+1][1]-mid_points[i][1]+1).astype(np.float32), 2.0)+np.math.pow(line_length//2+2, 2.0))
    #         ) / np.pi * 180.0
    #     )
    # if len(mid_gradients) == 0:
    #     print('no finger detected.')
    #     return None
    # average_mid_gradient = np.mean(mid_gradients)


    # start_point = (int(np.mean([item[1] for item in mid_points])), int(np.mean([item[0] for item in mid_points])))
    # end_point = (int(start_point[0]+GRADIENT_LINE_LENGTH_FOR_VIS * np.sin(average_mid_gradient * np.pi / 180.0)), int(start_point[1]+GRADIENT_LINE_LENGTH_FOR_VIS * np.cos(average_mid_gradient * np.pi / 180.0)))
    #
    # for x in range(image_sobel.shape[0]):
    #     for y in range(image_sobel.shape[1]):
    #         if image_sobel[x, y] == 1:
    #             image_sobel_draw[x, y, :] = (255, 255, 255)
    # cv2.arrowedLine(image_sobel_draw, end_point, start_point, color=(0, 0, 255), thickness=8, tipLength=0.3)
    # cv2.imwrite(osp.join(OUTPUT_PATH, 'test_222_{}.jpg'.format(item.split('/')[-1].split('.')[0])), image_sobel_draw)
    # cv2.imwrite(osp.join(OUTPUT_PATH, 'test_{}.jpg.jpg'.format(item.split('/')[-1].split('.')[0]))), image_sobel*255)
    # cv2.imwrite(osp.join(OUTPUT_PATH, '{}_{}_canny_as_filter.jpg'.format(item.split('.')[0], 'skin')), image_sobel)
    # cv2.imwrite(osp.join(OUTPUT_PATH, 'test_{}.jpg'.format(item.split('/')[-1].split('.')[0])), image_sobel*255)

    return theta




for item in os.listdir(INPUT_PATH):
    time_start_a = time.time()
    if '.jpg' not in item and '.png' not in item:
        print('not a valid image')
        continue
    image = cv2.imread(osp.join(INPUT_PATH, item))
    print('reading time: ', time.time() - time_start_a)

    time_start_b = time.time()
    average_mid_gradient = finger_recognition(image)
    print(average_mid_gradient)
    print('processing time: ', time.time() - time_start_b)


# import os
# start = time.time()
# for item in os.listdir(INPUT_PATH):
#     finger_recognition(item)
# end = time.time()
# print(1.0 / ((end - start) / len(os.listdir(INPUT_PATH))))






