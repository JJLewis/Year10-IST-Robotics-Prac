import cv2
import numpy as np
import time

img = cv2.imread('test5.jpg',0)
ret,thresh = cv2.threshold(img,127,255,0)
contours,hierarchy = cv2.findContours(thresh, 1, 2)

cnt = contours[0]
M = cv2.moments(cnt)
#print M

cx = int(M['m10']/M['m00'])
cy = int(M['m01']/M['m00'])
print cx
print cy

x,y,w,h = cv2.boundingRect(cnt)

cv2.imshow("Title of the little debug window", img)
time.sleep(3)

img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
#cv2.imshow("Title of the little debug window", img)
#time.sleep(3)