import cv2

cap = cv2.VideoCapture('IMG_3526.mp4')
i = 0
while (cap.isOpened()):
	ret, frame = cap.read()
	if ret == False:
		break
	if i%10 == 0: #extract every 10th frame of the video
		cv2.imwrite('currentframe.jpg', frame)
	i+=1
cap.release()
cv2.destroyAllWindows()