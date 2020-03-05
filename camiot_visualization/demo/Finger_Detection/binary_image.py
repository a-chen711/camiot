import numpy as np
import cv2 
from matplotlib import pyplot as plt

def binary_image_r(image_name,thre):
	#img_in = cv2.imread(image_dir)
	img = cv2.cvtColor(image_name.copy(),cv2.COLOR_BGR2GRAY)
	height,width = img.shape
	retval,mask_img = cv2.threshold(img, thre, 255, cv2.THRESH_BINARY)
	
	
	return mask_img

if __name__ == "__main__":
	img_in = cv2.imread('IF/5image.jpg',1)
	img = cv2.cvtColor(img_in.copy(),cv2.COLOR_BGR2GRAY)
	height, width= img.shape
	'''
	for line in range(height):
		for pixel in range(width):
			print((line,pixel,img[line,pixel]))
	'''

	img_out = binary_image_r(img_in,230)

	cv2.imshow('Grey image',img_out)
	cv2.waitKey(0)
	cv2.destroyAllWindows()