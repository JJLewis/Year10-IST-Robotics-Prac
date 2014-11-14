import numpy as np
import cv2
import time

video = cv2.VideoCapture().open('tennisball.mov')
cv2.imshow('Video',video)