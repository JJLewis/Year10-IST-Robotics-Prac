import cv2
import numpy as np
import sys
import libardrone.libardrone as libardrone
import PIL.Image as Image
import pygame

W, H = 1280, 720
topCamFrame = []
botCamFrame = []

def findBall(): # Find Red Ball
	pass

def findDot(): # Find Red Dot on the floor
	pass

def main():
	
	# Initiate Drone
	drone = libardrone.ARDrone(True, True)
	drone.reset()
	drone.set_camera_view(True) # False for bottom camera
	
	running = True
	while running:
		try:
			# Fetch numpy image array
			pixelarray = drone.get_image()
			if pixelarray != None:
				# Convert RGB to BGR & make OpenCV Image
				frame = pixelarray[:, :, ::-1].copy()
		except:
			print 'Frame Fetch Failed'
	
	# Shutdown
	print 'Shutting down...'
	drone.halt()
	print 'Ok.'

if __name__ == '__main__':
	main()