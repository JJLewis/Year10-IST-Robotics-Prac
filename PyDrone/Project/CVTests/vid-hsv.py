import numpy as np
import cv2

cap = cv2.VideoCapture(0)

TARGET_COLOR_MIN = np.array([35,50,50], np.uint8) # Green -> 35,50,50
TARGET_COLOR_MAX = np.array([60,255,255], np.uint8) # Green -> 60,255,255

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    _frame = np.asarray(frame)
    frameHSV = cv2.cvtColor(_frame, cv2.COLOR_RGB2HSV)
    frameThreshold = cv2.inRange(frameHSV, TARGET_COLOR_MIN, TARGET_COLOR_MAX)
    
    element = cv2.getStructuringElement(cv2.MORPH_RECT,(1,1))
    frameThreshold = cv2.erode(frameThreshold,element, iterations=1)
    frameThreshold = cv2.dilate(frameThreshold,element, iterations=1)
    frameThreshold = cv2.erode(frameThreshold,element)
    
    frameThreshold = cv2.GaussianBlur(frameThreshold,(5,5),0)
    
    cv2.imshow('frame', frameThreshold)
    
    contours, hierarchy = cv2.findContours(frameThreshold,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    showingCNTs = []
    areas = []
    
    # Find Specific contours
    for cnt in contours:
	    approx = cv2.approxPolyDP(cnt,0.1*cv2.arcLength(cnt,True),True)
	    if len(approx)==4:
	    	area = cv2.contourArea(cnt)
	    	if area > 300:
	    		
	    		areas.append(area)
	    		showingCNTs.append(cnt)
	    		
	    		#print "square"
	    		cv2.drawContours(frame,[cnt],0,(0,0,255),-1)
	    		x,y,w,h = cv2.boundingRect(cnt)
	    		cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
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
    '''	'''
    if len(areas)>0:
	    m = max(areas)
	    maxIndex = [i for i, j in enumerate(areas) if j == m]
	    cnt = showingCNTs[maxIndex]
	    cv2.drawContours(frame,[cnt],0,(0,0,255),-1)
	    x,y,w,h = cv2.boundingRect(cnt)
	    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)    
    #cv2.drawContours(frame, contours, -1, (0,0,255), 3)
    '''
	
    # Display the resulting frame
    #cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()