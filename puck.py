import numpy as np
import math

# The class to represent a puck for an air hockey table.
class Puck:

    def __init__(self, lower_range, upper_range):
        self.__lower_range = lower_range
        self.__upper_range = upper_range
        self.__velocity = None
        self.__center = (0,0)
        self.__lastCenter = (0,0)
        self.__radius = None

    # Get the lower range of HSV.
    def get_lower(self):
        return self.__lower_range

    # Get the upper range of HSV.
    def get_upper(self):
        return self.__upper_range

    # Set the center for the puck.
    def set_center(self, newCenter):
        self.__lastCenter = center
        self.__center = newCenter
        
    # Set the radius of the puck.
    def set_radius(self, radius):
        self.__radius = radius
        
    # Get the center of the puck.
    def get_center(self):  
        return self.__center

        # Get the center of the puck.
    def get_lastCenter(self):  
        return self.__center
        
      
    # Calculate the speed and direction of the puck.
    def calculate_velocity(self, time):
       if len(self.__centers) == 2:
           center1 = self.__centers[0]
           center2 = self.__centers[1]
           x1 = center1[0]
           y1 = center1[1]
           x2 = center2[0]
           y2 = center2[1]
           
           x_min = (x2 + x1)/2 - (x2 + x1)/2 * .004
           x_max = (x2 + x1)/2 + (x2 + x1)/2 * .004
           y_min = (y2 + y1)/2 - (y2 + y1)/2 * .004
           y_max = (y2 + y1)/2 + (y2 + y1)/2 * .004
           
           velocity = 0
           
           if x_min <= x2 <= x_max and y_min <= y2 <= y_max and x_min <= x1 <= x_max and y_min <= y2 <= y_max:
               velocity = 0
           else:
               velocity = math.sqrt((math.pow(x2-x1,2)+(math.pow(y2-y1,2))))/time
               
               velocity = (2.5 / self.__radius) * velocity      
               
               velocity = format(velocity,'.2f')
           
               self.__velocity = velocity  
               
               return velocity
       pass
            
           
    # Calculate the intercept distance from puck to robot.
    def calculate_intercept_distance_to_robot(self, xpos, ypos, endPos):
        
        if self.__radius != None:
            xf, yf = endPos
        
            distance = math.sqrt(math.pow(xpos - xf, 2) + math.pow(ypos - yf, 2))
        
            distance = (2.5 / self.__radius) * distance - 10 
        
            distance = format(distance,'.2f')
        
            self.__distance = distance 
        
            return distance
        else:
            pass
    
    # Calculate the time the puck needs to hit the robot.
    def calculate_time_to_reach_robot(self):
        
        if self.__velocity == None:
            return
        
        if int(float(self.__velocity)) == 0:
            return
        
        # V = d/t,
        if  int(float(self.__velocity)) != 0 or self.__velocity != None:
            
            self.__time = float(self.__distance) / float(self.__velocity)
            
            self.__time = format(self.__time,'.2f')
            
            return self.__time
        else:
            pass
    
   
    