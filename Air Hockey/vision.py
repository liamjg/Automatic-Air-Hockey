import cv2
import numpy as np
import time
import math
from imutils.video import FPS
from puck import Puck
from comm import Comm

# The class to represent a computer vision for an air hockey table.
class Vision:

    def __init__(self):
        # Create and define a range of color in HSV for the air hockey puck.
        self.puck = Puck(np.array([136, 66, 46]),np.array([255, 255, 255]))
        self.video_capture = cv2.VideoCapture(0, cv2.CAP_V4L)

    # Get the frame.
    def get_frame(self):
        ret, frame = self.video_capture.read()
        if ret:
            pass
        return frame

    # Release the resources from the camera.
    def release_video_capture(self):
        self.video_capture.release()

    # Get the puck.
    def get_puck(self):
        return self.puck
    
    # Set the resolution of the camera.
    def set_resolution(self, res1, res2):
        self.video_capture.set(3, res1)
        self.video_capture.set(4, res2)
        
    # Get the frames per second.    
    def get_fps(self):
        return self.video_capture.get(cv2.CAP_PROP_FPS)
    
    # Set the frames per second.
    def set_fps(self,fps):
        self.video_capture.set(cv2.CAP_PROP_FPS, fps)
        
    def selectROI(self):
        return cv2.selectROI("Region",self.video_capture.read()[1])

def main():
    # Create a vision object.
    vision = Vision()
    
    # Create a communication object.
    comm = Comm()
    
    # Set the resolution to be 320 x 240.
    vision.set_resolution(320, 240)
    
    # Set the fps to 40.
    vision.set_fps(40)
    
    # Select a region of the air hockey table for reference points.
    region = vision.selectROI()
    
    # Variable to keep track number of frames.
    number_of_frames = 0
    
    # The start time.
    start = 0
    
    # The end time.
    end = 0
    
    # Slope queue
    slopes = []
    
    #x pos
    xpos = 0
    
    #y pos
    ypos = 0
    
    #end position
    endPos = (0, 0)
    
    #counter
    counter = 0
    
    #smoothing factor
    SMOOTH = 30
    
    # initialize the FPS throughput estimator
    fps = None

    # Infinite loop.
    while (True):
        
        fps = FPS().start()
        
        if number_of_frames == 0:
            # Start timer for time delay between camera frames.
            start = time.time()
            
        number_of_frames = number_of_frames + 1
        
        # Take each frame
        frame = vision.get_frame()
        
        # Take a crop of a frame
        frame_crop = frame[int(region[1]):int(region[1] + region[3]), int(region[0]):int(region[0] + region[2])]
    
        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame_crop, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, vision.get_puck().get_lower(), vision.get_puck().get_upper())

        # RETR_EXTERNAL to extract only outer contours, useful for circles.
        contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Initialize center.
        center = (0,0)
        lastCenter = center

        if len(contours) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            # Find moments - each pixel in image has weight that is equal to its intensity.
            # Then the point you defined is centroid (center of mass) of image
            M = cv2.moments(c)

            # Divison by 0
            if M["m00"] != 0:
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # only proceed if the radius meets a minimum size
            if radius > 6 and center is not (0,0):
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                # (image,center,radius,color,thickness)
                cv2.circle(frame_crop, (int(x), int(y)), int(radius),
                           (0, 255, 255), 1)
                cv2.circle(frame_crop, center, 0, (0, 0, 255), -1)
                # Set the center of the puck.
                
                if(abs((center[0] - lastCenter[0])) > SMOOTH and abs((center[1] - lastCenter[1])) > SMOOTH):
                    vision.get_puck().set_center(center)
                
                # Set the radius of the puck.
                vision.get_puck().set_radius(radius)    
            
        # Prediction Line, for ever 4 frames calculate slope and draw a prediction line using the slope.
        if len(vision.get_puck().get_centers()) == 2:
            vision.get_puck().get_centers().clear()
             
        if center is not (0,0) and center is not None:
            vision.get_puck().get_centers().append(vision.get_puck().get_center())
             
        if len(vision.get_puck().get_centers()) == 2 and center is not (0,0):
            center1 = vision.get_puck().get_centers()[0]
            center2 = vision.get_puck().get_centers()[1]
            x1 = center1[0]
            y1 = center1[1]
            x2 = center2[0]
            y2 = center2[1]
            
            x_average = (x1 + x2) / 2
            x_sig = (x1 + x1 * .05)
            
            # If the puck is moving towards the robot.
            if x2 > x1:
                
                # Exclude division by 0.
                if x2 != x1:
                    # Slope formula
                    m = (y2 - y1) / (x2 - x1)
                    slopes.append(m)
                    
                    # The x position of the robot.
                    x = region[2]+region[0]
                    
                    # The y position where the robot intercept the puck.
                    y = m * (x - x2) + y2
                    
                    # The point where the robot intercept the puck.
                    end = (int(x),int(y))
                    
                    if len(slopes) == 2:
                        
                        #if x_sig >= x_average:
                        #    endPos = (int(x),int(y))
                        #    xpos = x2
                        #    ypos = y2
                        #    pass
                        
                        #if slope is positive
                        if slopes[0] > 0:
                        #if slope changes update end position
                            if slopes[1] < 0:
                                endPos = (int(x),int(y))
                                xpos = x2
                                ypos = y2
                            
                        #if slope is negative
                        if slopes[0] < 0:
                            #if slope change update end position
                            if slopes[1] > 0:
                                endPos = (int(x),int(y))
                                xpos = x2
                                ypos = y2
                                
                        
                        if counter == 4:
                            endPos = (int(x),int(y))
                            xpos = x2
                            ypos = y2
                    
                    if len(slopes) == 2:
                        slopes.pop(0)

               
        
        cv2.line(frame_crop, (xpos,ypos), endPos, (0,255,0),2)
        
        # Send position to robot to block puck.
        if (50 <= endPos[1] <= 100):
            comm.run(math.floor((endPos[1]-50)/12.5))
        elif(endPos[1] < 50):
            comm.run('0')
        elif(endPos[1] > 100):
            comm.run('4')
        
        
        
        # Need two frames to calculate velocity.
        if len(vision.get_puck().get_centers()) == 2:
            end = time.time()
            
            # Time delay between two centers.
            time_delay = end - start
            
            # Calculate the velocity of the puck.
            velocity = vision.get_puck().calculate_velocity(time_delay)
            
            cv2.putText(frame_crop,'Velocity: ' + str(velocity) + ' cm/s',(20,20),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,0,255),1,cv2.LINE_AA)
            
            number_of_frames = 0
            
            # Calculate the intercept distance from puck to robot.
            intercept_distance = vision.get_puck().calculate_intercept_distance_to_robot(xpos,ypos,endPos)
    
            cv2.putText(frame_crop,'Distance: ' + str(intercept_distance) + ' cm',(20,40),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,0,255),1,cv2.LINE_AA)

            intercept_time = vision.get_puck().calculate_time_to_reach_robot()
        
            cv2.putText(frame_crop,'Time: ' + str(intercept_time) + ' s',(20,60),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,0,255),1,cv2.LINE_AA)

        fps.update()
        fps.stop()
        
        fps = format(fps.fps(),'.2f')
        cv2.putText(frame_crop,'FPS: ' + fps + ' s',(20,80),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,0,255),1,cv2.LINE_AA)

        # Show camera frame.
        cv2.imshow('Frame', frame)
         
        # Show the cropped frame.
        cv2.imshow('Crop Frame',frame_crop)
        
        counter += 1
        if counter == 5:
            counter = 0

        # Quit the loop.
        if cv2.waitKey(1)& 0xFF == ord('q'):
            
            # Close the serial communication to the robot.
            comm.close_serial()
            
            break


if __name__ == "__main__":
    main()
    
    # Close and destroy processes for the windows.
    cv2.destroyAllWindows()
