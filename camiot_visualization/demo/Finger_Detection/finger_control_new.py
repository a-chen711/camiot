import numpy as np
import cv2 
# from pyimagesearch import imutils
from matplotlib import pyplot as plt

def finger_control_f_new(img_dir, threshold, strict=50):
	image = cv2.imread(img_dir)
	height,width,_ = image.shape
	height = int(height/2)
	# use only the lower half
	image = image[height:]
	bg = image.copy()
	bg[:,:,:] = 0
	bg2 = bg.copy()

	# sharpen and edge
	kernel_sharpening = np.array([[-1,0,-1], 
                              [-1, 7,-1],
                              [-1,0,-1]])
	sharpened = cv2.filter2D(image, -1, kernel_sharpening)

	gray = cv2.cvtColor(sharpened, cv2.COLOR_BGR2GRAY)
	gray = cv2.bilateralFilter(gray, 11, 17, 17)
	edged = cv2.Canny(gray, 30, 200)

	# blur the background
	im2, contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cv2.drawContours(bg, contours, -1, (0,255,0), 1)
	smooth = np.ones((30, 30), np.float32) / (30*30) * 10
	bg = cv2.filter2D(bg, -1, smooth)

	# edge again
	gray2 = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)
	ret, thresh = cv2.threshold(gray2, 127, 255, 0)
	im3, contours2, hierarchy2 = cv2.findContours(gray2.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cv2.drawContours(bg2, contours2, -1, (255,255,0), 1)

	# find the lines in the background2
	bg3 = bg2[:,:,0].copy()
	mid_record = []
	width_record = []
	prev_point = 0
	mid_point = 0
	mid_width = 0
	toggle = False
	# middle point at the bottom line
	h_poin_o = height-10
	bott_mid = []
	bott_width = []
	for w_point in range(10,width-10):
		if bg3[h_poin_o, w_point] > 0 and toggle:
			mid_point = int((prev_point + w_point)/2)
			mid_width = w_point - prev_point 
			bott_mid.append(mid_point)
			bott_width.append(mid_width)
			prev_point = w_point
			toggle = False
		elif bg3[h_poin_o, w_point] == 0:
			toggle = True
		else:
			toggle = toggle
	bg3[h_poin_o, bott_mid] = 255
	# search middle point for each line
	max_height = []
	max_top = []
	top_mid = []
	slope = []
	for start_point,start_width in zip(bott_mid,bott_width):
		flag_default = True
		mid_list = [start_point]
		width_list = [start_width]
		new_mid_point = start_point
		new_height = h_poin_o-5
		for h_point in range(h_poin_o-5,15,-1):
			# check if the width of the area is too small, break
			if start_width < int(width/5):
				print('break at ', h_point, start_point)
				top_mid.append(start_point)
				flag_default = False
				# max_height.append(new_height)
				break
			# left
			left = 0
			right = 0
			for x in range(new_mid_point, np.max([new_mid_point-int(width/4),0]), -1):
				if bg3[h_point, x]  > 0:
					left = x
					break
			# right
			for x in range(new_mid_point, np.min([new_mid_point+int(width/4),width]), 1):
				if bg3[h_point, x]  > 0:
					right = x
					break
			mid_line = int((left+right)/2)
			width_line = right-left
			# not to ruin the image, we slightly shift the display
			bg3[h_point+1, mid_line] = 255
			# end condition - large variance
			if np.abs(mid_line-mid_list[-1]) > int(width/strict) or width_line > width_list[-1]+int(width/(strict*1.5)):
				print('break at ', h_point, mid_list[-1])
				top_mid.append(mid_list[-1])
				flag_default = False
				# max_height.append(new_height)
				break
			else:
				mid_list.append(mid_line)
				width_list.append(width_line)
				new_mid_point = mid_line
				new_height = h_point
		if flag_default:
			top_mid.append(start_point)
		# compute the top bounded point
		real_upper_point = new_height
		real_h_point = new_height
		if new_height < (height - threshold):
			for h_upper_point in range(new_height,np.max([new_height-int(height/4),0]),-1):
				if bg3[h_upper_point, mid_list[-1]] > 0:
					print(h_upper_point, mid_list[-1])
					real_h_point = new_height
					real_upper_point = h_upper_point
					break
				else:
					real_h_point = height-10
					real_upper_point = height-10
					bg3[h_upper_point, mid_list[-1]] = 255
		max_height.append(real_h_point)
		max_top.append(real_upper_point)
		

	# compute slope k 
	k_height = np.array(max_height)
	k_mid_top = np.array(top_mid)
	k_mid_bott = np.array(bott_mid)
	print(k_mid_top,k_mid_bott)
	slope = (height-10. - k_height)/(k_mid_top - k_mid_bott)

	# information of all lines
	print(max_height)
	print(max_top)
	print(bott_mid)
	print(top_mid)
	print(slope)

	if not max_height:
		height_out, top_out, bott_out, topmid_out,slope_out = height,height,0,0,0
	else:
		out_index = np.argmin(max_top)
		print('index',out_index)
		height_out = max_height[out_index]
		top_out = max_top[out_index]
		bott_out = bott_mid[out_index]
		topmid_out = top_mid[out_index]
		slope_out = slope[out_index]
		bg3[top_out:top_out+9,topmid_out:topmid_out+9] = 255
	return bg3, height_out, top_out, bott_out, topmid_out, slope_out
'''
if __name__ == "__main__":

	# img_bk,k,top,mid,control, bottom_mid = finger_control_f('IRBOT1crp.jpg',200, 30,-70,3)
	# print('slope is ',k,'top y value is ',top, 'mid value is ', mid)
	# print('control signal is', control)

	img_bk, height_out, top_out, bott_out, topmid_out, slope_out = finger_control_f_new('47OhmOFFcrp.jpg',50,50) 
	# img_bk, height_out, top_out, bott_out, topmid_out, slope_out = finger_control_f_new('7image.jpg',50,50) 
	# img_bk, height_out, top_out, bott_out, topmid_out, slope_out = finger_control_f_new('IRBOT1crp.jpg',50,50)
	print('result: measured top ', height_out,' max top ',top_out,' bottom middle ', bott_out,\
		' top middle ' , topmid_out, ' slope ',slope_out)
	cv2.imshow('Binary Image', img_bk)

	cv2.waitKey(0)
'''