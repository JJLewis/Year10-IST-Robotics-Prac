import numpy as np
import cv2
import sys
import libardrone.libardrone as libardrone
import PIL.Image as Image
import time

def main():
	W, H = 1280, 720
	
	drone = libardrone.ARDrone(True, True)
	drone.reset()
	drone.set_camera_view(True) # False for bottom camera
	
	running = True
	while running:
		try:
			drone.set_camera_view(True)
			# This should be an numpy image array
			pixelarray = drone.get_image()
			if pixelarray != None:
				# Convert RGB to BGR
				open_cv_image = pixelarray[:, :, ::-1].copy()
				# Display the Image
				cv2.imshow('Drone', open_cv_image)
				
				#time.sleep(1)
				# Switch the camera
				drone.set_camera_view(False)
				try:
					botpixelarray = drone.get_image()
					if botpixelarray != None:
						botCamImage = botpixelarray[ :, :, ::-1].copy()
						cv2.imshow('a', botCamImage)
				except:
					pass
		except:
			print "Failed"
		
		# Wait for next frame
		time.sleep(0.05)
		# Listen for Q Key Press
		if cv2.waitKey(1) & 0xFF == ord('q'):
			running = False
	print "Shutting Down..."
	drone.halt()
	print "Ok."
	
if __name__ == '__main__':
	main()