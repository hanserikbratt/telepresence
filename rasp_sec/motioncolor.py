# To run the raspberry pi 2 camera using openCVs Videocapture the 
# UV4L drivers need to be install, a guide on how to do this can be found on
# http://www.linux-projects.org/modules/sections/index.php?op=viewarticle&artid=14

# import the necessary packages
import imutils
import time
import cv2
import numpy as np

# init-method initializing variables.
def init():
    global cx
    global cy
    global camera
    cx = 0
    cy = 0
 
 # initializing the RPI camera using openCVs VideoCapture 
    camera = cv2.VideoCapture(0)
    time.sleep(0.25)

# get-method returning x and y offset in pixels from centrum 
def getdata():
    # grab the current frame and initialize the occupied/unoccupied
    (grabbed, frame) = camera.read()
 
    # if the frame could not be grabbed, then we have reached the end
    # of the video
    if not grabbed:
        print "Error no frame"

    frame = imutils.resize(frame, width=320)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # define range of magenta in HSV in which the mask
    # should be constructed
    lower_magenta = np.array([170,100,50])
    upper_magenta = np.array([180,255,255])

    # Threshold the HSV image to get only magenta colors
    mask = cv2.inRange(hsv, lower_magenta, upper_magenta)
    
    M = cv2.moments(mask)
    if M['m00'] != 0:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
    else :
    # Setting the xp and yp as the deviation
    # from the center of the picture 
        cx = 160
        cy = 120 
    xp = cx-160
    yp = cy-120

    return xp, yp
# Method to release the camera
def kill():
    global camera
# release and kill camera.
    camera.release()

        
