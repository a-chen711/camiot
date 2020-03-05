#https://www.pyimagesearch.com/2017/06/19/image-difference-with-opencv-and-python/


import numpy as np
from skimage import filters
from skimage.measure import compare_ssim  
from skimage.segmentation import flood, flood_fill
import argparse
import imutils
import cv2
import matplotlib.pyplot as plt  

def direction(image):
	height, width = image.shape
	white_areas = []
	start_point = 8
	current_point = 8
	white_thr = 230
	black_thr = 10

	# get the white range for each line
	for pixel in range(4,width-4,4):
		#print((pixel,img[height-1,pixel]))
		if img[height-1,pixel] >white_thr:
			if img[height-1, pixel - 4] < black_thr :
				start_point = pixel
			elif img[height-1, pixel - 4] >white_thr or img[height-1, pixel + 4] > white_thr:
				current_point = pixel
			
			if pixel > width - 9:
				current_point = pixel
				white_areas.append((start_point,current_point))
		elif img[height-1,pixel] < black_thr:
			if img[height-1, pixel - 4] >white_thr and start_point < current_point:
				white_areas.append((start_point,current_point))
	#print('White areas: ',white_areas)
	# if no white area, return the original image
	print(white_areas)
	if white_areas ==[]:
		#print('line 42 termination')
		general_k = 1000
		to_crop_v = height / 2
		to_crop_h = width / 2
		control_signal = 'Down'
		return img, general_k, to_crop_v, to_crop_h, control_signal, None
	# find the mean point of each line
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


def masking(image,thre):
	output=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	#output=cv2.adaptiveThreshold(output, 255, cv2.cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11,2)
	retval,output=cv2.threshold(output,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	return output

def fingerFinder():
	ap=argparse.ArgumentParser()
	ap.add_argument("-f", "--first", required=True,help="first input image")
	#ap.add_argument("-s", "--second", required=True,help="second input image")
	args = vars(ap.parse_args())
	thre=200
	print("stopped")

	#load the image 
	ir=cv2.imread(args["first"])	
	#noIr=cv2.imread(args["second"])
	#convert the image to grayscale 
	irOut=masking(ir,thre)
	#noIrOut=masking(noIr,thre)
	print("stopped")
	cv2.imwrite("results/irOut_test.jpg",irOut)
	#cv2.imwrite("results/noirOut_test.jpg",noIrOut)
	print("complete")

def imagediff():
	ap = argparse.ArgumentParser()
	ap.add_argument("-f", "--first", required=True,
	help="first input image")
	ap.add_argument("-s", "--second", required=True,
	help="second")
	args = vars(ap.parse_args())
	
	imageA = cv2.imread(args["first"])
	imageB = cv2.imread(args["second"])
	cropA = imageA[240:480, 0:480]
	cropB = imageB[240:480, 0:480]
	grayA = cv2.cvtColor(cropA, cv2.COLOR_BGR2GRAY)
	grayB = cv2.cvtColor(cropB, cv2.COLOR_BGR2GRAY)

	

	(score, diff) = compare_ssim(grayA, grayB, full=True)
	diff = (diff * 255).astype("uint8")
	print("SSIM: {}".format(score))
	
	# threshold the difference image, followed by finding contours to
# obtain the regions of the two input images that differ
	thresh = cv2.threshold(diff, 0, 255,
		cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)

	# loop over the contours
	for c in cnts:
	# compute the bounding box of the contour and then draw the
	# bounding box on both input images to represent where the two
	# images differ
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(cropA, (x, y), (x + w, y + h), (0, 0, 255), 2)
		cv2.rectangle(cropB, (x, y), (x + w, y + h), (0, 0, 255), 2)
	# show the output images
	cv2.imshow("Original", cropA)
	cv2.imshow("Modified", cropB)
	cv2.imshow("Diff", diff)
	cv2.imshow("Thresh", thresh)
	cv2.waitKey(0)


def image_bright():
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--image", help = "path to the image file")
	ap.add_argument("-r", "--radius", type = int,
		help = "radius of Gaussian blur; must be odd")
	args = vars(ap.parse_args())
	# load the image and convert it to grayscale
	image = cv2.imread(args["image"])
	orig = image.copy()
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	# perform a naive attempt to find the (x, y) coordinates of
	# the area of the image with the largest intensity value
	(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
	cv2.circle(image, maxLoc, 5, (255, 0, 0), 2)
	# display the results of the naive attempt
	#cv2.imshow("Naive", image)
	# apply a Gaussian blur to the image then find the brightest
	# region
	gray = cv2.GaussianBlur(gray, (args["radius"], args["radius"]), 0)
	(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
	cv2.imshow("Grayscale", gray)
	image = orig.copy()
	cv2.circle(image, maxLoc, args["radius"], (255, 0, 0), 2)
	# display the results of our newly improved method
	cv2.imshow("Robust", image)
	cv2.waitKey(0)

def floodfill():
	ir_in = cv2.imread("Test2.jpg", cv2.IMREAD_GRAYSCALE);

	th, ir_th = cv2.threshold(ir_in, 220, 255, cv2.THRESH_BINARY_INV);

	ir_floodfill = ir_th.copy()

	h, w = ir_th.shape[:2]
	mask = np.zeros((h+2, w+2),np.uint8)

	cv2.floodFill(ir_floodfill, mask, (0,0), 255);
	ir_floodfill_inv = cv2.bitwise_not(ir_floodfill)

	ir_out = ir_th | ir_floodfill_inv

	cv2.imshow("Flood", ir_floodfill)
	#cv2.imshow("Threshold", ir_th)
	cv2.imshow("Inverted Floodfill", ir_floodfill_inv)
	cv2.imshow("Foreground", ir_out)
	cv2.waitKey(0)






'''
def example():
	# construct the argument parse and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-f", "--first", required=True,
		help="first input image")
	ap.add_argument("-s", "--second", required=True,
		help="second")
	args = vars(ap.parse_args())

	# load the two input images
	imageA = cv2.imread(args["first"])
	imageB = cv2.imread(args["second"])
	# convert the images to grayscale
	grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
	grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
	cv2.imshow("imag1",grayA)
	cv2.imshow("imag2",grayB)

	(score, diff) = compare_ssim(grayA, grayB, full=True)

	diff = (diff * 255).astype("uint8")
	print("SSIM: {}".format(score))
	cv2.imshow("difference",diff)

	# threshold the difference image, followed by finding contours to
	# obtain the regions of the two input images that differ
	thresh = cv2.threshold(diff, 0, 255,
		cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)

	cnts = imutils.grab_contours(cnts)

	# loop over the contours
	for c in cnts:
		# compute the bounding box of the contour and then draw the
		# bounding box on both input images to represent where the two
		# images differ
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
		cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)
	# show the output images
	cv2.imwrite("output/Original.jpg", imageA)
	cv2.imwrite("output/Modified.jpg", imageB)
	cv2.imwrite("output/Diff.jpg", diff)
	cv2.imwrite("output/Thresh.jpg", thresh)
	cv2.waitKey(10000000)
	cv2.destroyAllWindows()
'''

#fingerFinder()
#imagediff()
#image_bright()
floodfill()
#example()

	