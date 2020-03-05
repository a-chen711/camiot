import numpy as np
import cv2 
from matplotlib import pyplot as plt
from binary_image import binary_image_r

def subtract_green(img_1_in,img_2_in):
	img_1 = cv2.imread(img_1_in)
	img_2 = cv2.imread(img_2_in)

	height,width,channel = img_1.shape

	img_out = np.zeros([height,width,channel],dtype=np.uint8)
	img_out.fill(0)
	
	for line in range(height):
		for pixel in range(width):
			#print((line,pixel),(img_1[line,pixel][1],img_2[line,pixel][1],max([img_1[line,pixel][1],img_2[line,pixel][1]])-min([img_1[line,pixel][1],img_2[line,pixel][1]])))
			if max([img_1[line,pixel][1],img_2[line,pixel][1]])-min([img_1[line,pixel][1],img_2[line,pixel][1]])>30:
				img_out[line,pixel][1] = 255
				
	return img_out

if __name__ == "__main__":
	img_1 = cv2.imread('LEDs/1.jpg')
	img_2 = cv2.imread('LEDs/2.jpg')
	'''
	img_1 = cv2.fastNlMeansDenoisingColored(img_1,None,10,10,7,21)
	img_2 = cv2.fastNlMeansDenoisingColored(img_2,None,10,10,7,21)
	'''
	height,width,channel = img_1.shape

	img_out = np.zeros([height,width,channel],dtype=np.uint8)
	img_out.fill(0)
	
	for line in range(height):
		for pixel in range(width):
			#print((line,pixel),(img_1[line,pixel][1],img_2[line,pixel][1],max([img_1[line,pixel][1],img_2[line,pixel][1]])-min([img_1[line,pixel][1],img_2[line,pixel][1]])))
			if max([img_1[line,pixel][1],img_2[line,pixel][1]])-min([img_1[line,pixel][1],img_2[line,pixel][1]])>30:
				img_out[line,pixel][1] = 255
	
	#img_out[:,:,1] = img_1[:,:,1] - img_2[:,:,1]

	#img_out = cv2.fastNlMeansDenoisingColored(img_out,None,10,10,7,21)
	#cv2.imwrite('Green Channel Reduction.jpg', img_out)
	#cv2.imshow('Green Image', img_out)

	img_final = binary_image_r(img_out)
	cv2.imshow('Final Image', img_final)
	cv2.imwrite('Binary_Image.jpg', img_final)
	#cv2.imshow('Grey Image', img_grey)


	cv2.waitKey(0)
	cv2.destroyAllWindows()

