import numpy as np
import cv2
import sys

cap = cv2.VideoCapture(0)

# RGB Colors
target_min = np.uint8([[[84,0,37]]])
target_max = np.uint8([[[233,62, 143]]])
hsv_min = cv2.cvtColor(target_min,cv2.COLOR_RGB2HSV)
hsv_max = cv2.cvtColor(target_max,cv2.COLOR_RGB2HSV)

TARGET_COLOR_MIN = np.array([120,50,50], np.uint8) # Green -> 35,50,50; Pink? -> 120,50,50; Blue -> 110 or 0; Skin Color -> 0
TARGET_COLOR_MAX = np.array([125,255,255], np.uint8) # Green -> 60,255,255; Pink? -> 180,255,255; Blue -> 130 or 15; Skin Color -> 120

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    _frame = np.asarray(frame)
    frameHSV = cv2.cvtColor(_frame, cv2.COLOR_RGB2HSV)
    frameThreshold = cv2.inRange(frameHSV, TARGET_COLOR_MIN, TARGET_COLOR_MAX)
    
    element = cv2.getStructuringElement(cv2.MORPH_RECT,(1,1))
    frameThreshold = cv2.erode(frameThreshold,element, iterations=1)
    frameThreshold = cv2.dilate(frameThreshold,element, iterations=1)
    frameThreshold = cv2.erode(frameThreshold,element)
    
    # Blurs to smoothen frame
    frameThreshold = cv2.GaussianBlur(frameThreshold,(9,9),2,2)
    frameThreshold = cv2.medianBlur(frameThreshold,5)
    
    '''
    # Find Circles and Draw them
    circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1.2, 100)
	# detect circles in the image
	#circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1.2, 100)
	
	# ensure at least some circles were found
    if circles is not None:
		# convert the (x, y) coordinates and radius of the circles to integers
		circles = np.round(circles[0, :]).astype("int")
 
		# loop over the (x, y) coordinates and radius of the circles
		for (x, y, r) in circles:
			# draw the circle in the output image, then draw a rectangle
			# corresponding to the center of the circle
			cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
			cv2.rectangle(frame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
	'''
    '''
    circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT,1,20, param1=50,param2=30,minRadius=5,maxRadius=20)
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
    	# draw the outer circle
    	cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
    	# draw the center of the circle
    	cv2.circle(frame,(i[0],i[1]),2,(0,0,255),3)
    '''
    #cv2.imshow('frame', frameThreshold)
    
    contours, hierarchy = cv2.findContours(frameThreshold,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    showingCNTs = []
    areas = []
    
    # Find Specific contours
    for cnt in contours:
	    approx = cv2.approxPolyDP(cnt,0.1*cv2.arcLength(cnt,True),True)
	    #if len(approx)==4:
	    area = cv2.contourArea(cnt)
	    if area > 600:
	    	
	    	areas.append(area)
	    	showingCNTs.append(cnt)
	    	'''
	    		#print "square"
	    		#cv2.drawContours(frame,[cnt],0,(0,0,255),-1)
	    		x,y,w,h = cv2.boundingRect(cnt)
	    		cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
	    	'''
	    '''
	    print len(approx)
	    if len(approx)==5:
	        print "pentagon"
	        cv2.drawContours(frame,[cnt],0,255,-1)
	    elif len(approx)==3:
	        print "triangle"
	        cv2.drawContours(frame,[cnt],0,(0,255,0),-1)
	    elif len(approx)==4:
	        print "square"
	        cv2.drawContours(frame,[cnt],0,(0,0,255),-1)
	    elif len(approx) == 9:
	        print "half-circle"
	        cv2.drawContours(frame,[cnt],0,(255,255,0),-1)
	    elif len(approx) > 15:
	        print "circle"
	        cv2.drawContours(frame,[cnt],0,(0,255,255),-1)
    '''
    # Only Highlight the largest object
    if len(areas)>0:
	    m = max(areas)
	    maxIndex = 0
	    for i in range(0, len(areas)):
	    	if areas[i] == m:
	    		maxIndex = i
	    		#print "Max Value: "+str(m)
	    		#print "This Value: "+str(areas[i])
	    		
	    cnt = showingCNTs[maxIndex]
	    
	    # Highlight the Object Red
	    #cv2.drawContours(frame,[cnt],0,(0,0,255),-1)
	    
	    # Draw a bouding rectangle
	    x,y,w,h = cv2.boundingRect(cnt)
	    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
	    
	    # Draw a rotated bounding rectangle
	    rect = cv2.minAreaRect(cnt)
	    box = cv2.cv.BoxPoints(rect)
	    box = np.int0(box)
	    cv2.drawContours(frame,[box],0,(0,255,255),2)
	    
	    # Draw a circumcircle
	    (x,y),radius = cv2.minEnclosingCircle(cnt)
	    center = (int(x),int(y))
	    radius = int(radius)
	    cv2.circle(frame,center,radius,(255,0,255),2)
	    
	    # Draw line to center of screen
	    screenMidX = 1280/2
	    screenMidY = 720/2
	    cv2.line(frame, (640, 360), center, (0,0,255),2)
	    
	    diff = 60
	    # Loop for drawing speed circles
	    for i in range(1, 10):
	    	cv2.circle(frame, (640, 360), diff*i,(0,0,255),2)
	    
	   	x = center[0]
	    y = center[1]	
	    # Loop for checking speed
	    for i in range(1, 10):
	    	area = (diff*i)^2
	    	pos = (x-640)^2+(y-360)^2-(diff*i)^2
	    	if pos <= area:
	    		# The point is inside circle
	    		print "Speed = " + str((i-1)/10)
	    		break
	    	if i == 10:
	    		if pos > 10:
	    			# The point is outside the circle
	    			print "Speed = 1.0"
	    			break
	    	
	     
    #cv2.drawContours(frame, contours, -1, (0,0,255), 3)
    
	
    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()