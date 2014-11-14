import cv2
import numpy as np
import time

im = cv2.imread('gimg.jpg')
imgray = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
ret,thresh = cv2.threshold(imgray,127,255,0)
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
c = cv2.drawContours(im, contours, -1, (0,255,0), 3)
cv2.imshow("Title of the little debug window", thresh)
time.sleep(3)