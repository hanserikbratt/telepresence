# To run the raspberry pi 2 camera using openCVs Videocapture the 
# UV4L drivers need to be install, a guide on how to do this can be found on
# http://www.linux-projects.org/modules/sections/index.php?op=viewarticle&artid=14
import argparse
import datetime
import imutils
import time
import cv2
 

def init():
    global cx
    global cy
    global camera
    global firstFrame
    cx = 0
    cy = 0
 # initializing the RPI camera using openCVs VideoCapture 
    camera = cv2.VideoCapture(0)
    time.sleep(0.25)
 
# initialize the first frame in the video stream
    firstFrame = None

def getdata():
    cx = 160 
    cy = 120
    global firstFrame
    # grab the current frame and initialize the occupied/unoccupied
    # text
    (grabbed, frame) = camera.read()
    text = "Unoccupied"
 
    # if the frame could not be grabbed, then we have reached the end
    # of the video
    if not grabbed:
        #break
        print "fel"
 
    # resize the frame, convert it to grayscale, and blur it
    frame = imutils.resize(frame, width=320)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # if the first frame is None, initialize it
    if firstFrame is None:
        firstFrame = gray
        #continue
        
    # compute the absolute difference between the current frame and
    # first frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 70, 255, cv2.THRESH_BINARY)[1]
 
    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    # loop over the contours
    for c in cnts:
        # if the contour is too small, ignore it
        #if cv2.contourArea(c) < args["min_area"]:
        #    continue
 
        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "Occupied"
        # draw the text and timestamp on the frame
    cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
        (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    if cnts:
        #
        firstFrame = None
        #time.sleep(0.5)
        M = cv2.moments(thresh)
        if M['m00'] != 0:
            cx = ( int(M['m10']/M['m00']))/1
            cy = ( int(M['m01']/M['m00']))/1
        else :
            cx = 1
            cy = 1


    xp = cx - 160
    xy = cy - 120

    

    return xp, xy


def kill():
    global camera
# cleanup the camera and close any open windows
    camera.release()
#cv2.destroyAllWindows()
#while True:
    #getdata()
        
