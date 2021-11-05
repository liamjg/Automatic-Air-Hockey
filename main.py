# import the necessary packages
from imutils.video import VideoStream
import imutils
import time
import cv2
import numpy

from puck import Puck

DEAD_ZONE = 30
CALC_FRAME_SKIP = 4



def getContours(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, puck.get_lower(), puck.get_upper())

    return cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

def getContourCenter(contours):
    c = max(contours, key=cv2.contourArea)
    M = cv2.moments(c)

    if M["m00"] != 0:
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
    else:
        return (0,0)

def getSlope(point1,point2):
    return (point2[1]-point1[1])/(point2[0]-point1[0])

# initialize the video stream and allow the cammera sensor to warmup
vs = VideoStream(usePiCamera=True).start()

time.sleep(2.0)

#initialize puck
puck = Puck(np.array([136, 66, 46]),np.array([255, 255, 255]))

#set region of interest
ROI = cv2.selectROI("Region", vs.read()[1])

frameCount = 0

lastSlope = -1

endPoint = (0,0)

# loop over the frames from the video stream
while True:
    # grab the frame from the threaded video stream and resize it
    # crop frame to selected ROI
    frame = vs.read()
    frame_crop = frame[int(ROI[1]):int(ROI[1] + ROI[3]), int(ROI[0]):int(ROI[0] + ROI[2])]

    frameCount += 1

    contours, hierarchy = getContours(frame_crop)
    
    center = getContourCenter(contours)

    #check calculated center for failed update or deadzone before setting
    if(center != (0,0)):
        #subtract the pucks current and last center, convert to abs, then subtract the deadzone
        diff = tuple(numpy.subtract(numpy.abs(numpy.subtract(center, puck.get_lastCenter())),DEAD_ZONE))

        if (diff[0] > 0 and diff[1] > 0):
            puck.set_center(center)



    #only recalc the slope if puck is moving toward the robot and no chance of div by 0
    if(puck.getCenter()[1] > puck.get_lastCenter()[1] and puck.getCenter()[0] != puck.get_lastCenter()[0]): 
        m = getSlope(puck.get_lastCenter(),puck.getCenter())

        x = region[2]+region[0]
                        
        # The y position where the robot intercept the puck.
        y = m * (x - puck.getCenter()[0]) +  puck.getCenter()[1]
                        
        #update endPoint on every nth frame or if slope changes
        if((frameCount % CALC_FRAME_SKIP == 0) or (m > 0 and lastSlope < 0) or (m < 0 and lastSlope > 0)):
            endPoint = (int(x),int(y))
            lastSlope = m

    cv2.line(frame_crop, puck.getCenter(), endPoint, (0,255,0),2)

    if (-16 <= endPos[1] <= 65):
        comm.run(3)
    elif (66 <= endPos[1] <= 90):
        comm.run(4)
    elif (91 <= endPos[1] <= 240):
        comm.run(5)


    # Show the cropped frame.
    cv2.imshow('Crop Frame',frame_crop)

    key = cv2.waitKey(1) & 0xFF
 
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
 
# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()