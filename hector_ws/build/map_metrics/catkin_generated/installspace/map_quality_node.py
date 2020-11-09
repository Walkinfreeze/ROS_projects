#!/usr/bin/env python2
import re
import numpy as np
import rospy
    
# license removed for brevity
from std_msgs.msg import Float64
from nav_msgs.msg import *


def callback(data):
    map_data = data
    map_ = np.array(map_data.data).reshape(map_data.info.height, map_data.info.width)

    free_ = 0;
    occupied_ = 0;
    for i in range(map_.shape[0]):
       for j in range(map_.shape[1]):
          if map_[i,j] > 60:
                  occupied_ += 1
                  map_[i,j]=0
          else:
                  free_ += 1
                  map_[i,j]=1
    grid = OccupancyGrid()
    grid.data = map_.ravel()
    grid.info = MapMetaData()
    grid.info.height = map_.shape[0]
    grid.info.width = map_.shape[1]

    pub1 = rospy.Publisher('binary_map', OccupancyGrid, queue_size=1)
    pub1.publish(grid)

    occupied_vector_ = []
    occupied_surface_vector_ = []
    free_vector_ = []
    free_surface_vector_ = []

    occupied_surface_ = occupied_ * map_data.info.resolution   
#    occupied_vector_.append(occupied_)
#    free_vector_.append(free_)
#    occupied_surface_vector_.append(occupied_surface_)
#    free_surface_vector_.append(free_surface_) 
    

    pub2 = rospy.Publisher('map_quality', Float64, queue_size=1)
    pub2.publish(occupied_surface_)
    
def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("map", OccupancyGrid, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
