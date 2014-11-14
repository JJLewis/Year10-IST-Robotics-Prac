import numpy as np
import cv2
import time

TARGET_COLOR_MIN = np.array([35,50,50], np.uint8)
TARGET_COLOR_MAX = np.array([60,255,255], np.uint8)

def main():
	ballImg = cv2.imread('test8.jpg')
	
	frame = np.asarray(ballImg)
	frameHSV = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
	frameThreshold = cv2.inRange(frameHSV, TARGET_COLOR_MIN, TARGET_COLOR_MAX)
	
	element = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
	frameThreshold = cv2.erode(frameThreshold,element, iterations=6)
	frameThreshold = cv2.dilate(frameThreshold,element, iterations=6)
	frameThreshold = cv2.erode(frameThreshold,element)
	
	ret,thresh = cv2.threshold(ballImg,127,255,0)
	contours,hierarchy = cv2.findContours(thresh, 1, 2)

	cnt = contours[0]
	M = cv2.moments(cnt)
	#print M
	
	cx = int(M['m10']/M['m00'])
	cy = int(M['m01']/M['m00'])
	
	print cx
	print cy
	
	'''
	contours, hierarchy = cv2.findContours(frameThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
 
	maximumArea = 0
	bestContour = None
	for contour in contours:
	    currentArea = cv2.contourArea(contour)
	    if currentArea > maximumArea:
	        bestContour = contour
	        maximumArea = currentArea
 
	if bestContour is not None:
	    x,y,w,h = cv2.boundingRect(bestContour)
	    cv2.rectangle(frame, (x,y),(x+w,y+h), (0,0,255), 3)
	'''
	cv2.waitKey(2)
	cv2.imshow("Title of the little debug window", frameThreshold)
	
	#cv2.imshow('Red Ball Image', ballImg)
	
	time.sleep(3)

if __name__ == '__main__':
	main()