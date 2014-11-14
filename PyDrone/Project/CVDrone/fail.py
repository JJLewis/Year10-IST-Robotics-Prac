import libardrone.libardrone as libardrone
import cv2
import numpy as np
import sys

import PIL.Image as Image

import pygame
import pygame.surfarray
import pygame.transform

def surf2CV(surf, cvImage):
	"""
	Given a Pygame surface, convert to an OpenCv cvArray format.
	Either Ipl image or cvMat.
	surf2CV( pygame.Surface src, cv.Image dest )
	(From http://facial-expression-recognition.googlecode.com/svn/trunk/code/conversion.py)
	( Extracted 2012-Jul-16 22:37EDT by GKF)
	"""
	from numpy import dsplit, dstack
	cv.Set(cvImage, (0,0,0))
	arr = pygame.surfarray.pixels3d(surf).transpose(1,0,2) # Reshape to 320x240
	r,g,b = dsplit(arr,3)
	arr = dstack((b,g,r))
	dtype2depth = {
	'uint8': cv.IPL_DEPTH_8U,
	'int8': cv.IPL_DEPTH_8S,
	'uint16': cv.IPL_DEPTH_16U,
	'int16': cv.IPL_DEPTH_16S,
	'int32': cv.IPL_DEPTH_32S,
	'float32': cv.IPL_DEPTH_32F,
	'float64': cv.IPL_DEPTH_64F,
	}
	try:
		nChannels = arr.shape[2]
	except:
		nChannels = 3
	try:
		cv.SetData(cvImage, arr.tostring(),arr.dtype.itemsize*nChannels*arr.shape[1])
	except:
		print "Error is: ",
		print sys.exc_info()[0]

def main():
	W, H = 320, 240
	
	pygame.init()
	screen = pygame.display.set_mode((W, H))
	clock = pygame.time.Clock()
	
	cap = cv2.VideoCapture().open('tcp://192.168.1.1:5555')
	
	drone = libardrone.ARDrone(True, False)
	drone.reset()
	drone.set_camera_view(False) # True for bottom camera
	running = True
	while running:
		ret, frame = cap.read()
		cv2.imshow('Drone', frame)
		'''
		try:
			pixelarray = drone.get_image()
			if pixelarray != None:
				#surface = pygame.surfarray.make_surface(pixelarray)
				#rotsurface = pygame.transform.rotate(surface, 270)
				#frame = surf2CV(rotsurface, frame)
				cv2.imshow('Drone', frame)
		except:
			pass
		'''
		'''
		try: pixelarray = drone.get_image()
			if pixelarray != None:
				# image is an numpy image array
				frame = Image.fromarray(drone.get_image())
				cv2.imshow('Drone', frame)
				#surface = pygame.surfarray.make_surface(pixelarray)
				#rotsurface = pygame.transform.rotate(surface, 270)
				#screen.blit(rotsurface, (0, 0))
		except:
			pass
		'''	
		#pygame.display.flip()
        #clock.tick(50)
        #pygame.display.set_caption("FPS: %.2f" % clock.get_fps())
        if cv2.waitKey(1) & 0xFF == ord('q'):
        	running = False
	
if __name__ == '__main__':
	main()
