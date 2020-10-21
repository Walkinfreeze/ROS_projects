#!/usr/bin/env python
import re
import numpy as np
import rospy

import os
from os import listdir
from os.path import isfile,join
import csv
import sys
from matplotlib import pyplot as plt
import matplotlib.animation as animation

from nav_msgs.msg import *
import datetime
import shutil

datetime_object = datetime.datetime.now()
np.set_printoptions(threshold=np.inf)

#occupied_vector_ = []
#occupied_surface_vector_ = []
#free_vector_ = []
#free_surface_vector_ = []

my_path = os.path.normpath(os.getcwd() + os.sep + os.pardir+'/'+'hector_ws'+'/'+'src'+'/'+'map_metrics'+'/'+'figures')

os.mkdir(os.path.normpath(os.getcwd() + os.sep + os.pardir+'/'+'hector_ws'+'/'+'src'+'/'+'map_metrics'+'/'+'figures'+'/'+str(datetime_object)))
my_path1 = os.path.normpath(os.getcwd() + os.sep + os.pardir+'/'+'hector_ws'+'/'+'src'+'/'+'map_metrics'+'/'+'figures'+'/'+str(datetime_object))


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
    occupied_vector_ = []
    occupied_surface_vector_ = []
    free_vector_ = []
    free_surface_vector_ = []

    occupied_surface_ = occupied_ * map_data.info.resolution 
    free_surface_ = free_ * map_data.info.resolution    
    occupied_vector_.append(occupied_)
    free_vector_.append(free_)
    occupied_surface_vector_.append(occupied_surface_)
    free_surface_vector_.append(free_surface_)
  
    X = np.arange(len(free_vector_))  
    plt.plot(occupied_surface_vector_, X, '*')
    plt.axis("equal")
    plt.draw()



    
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True) 
    rospy.Subscriber("map", OccupancyGrid, callback)
    plt.ion()
    plt.show()



    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    # listener() 
    rospy.init_node('listener', anonymous=True) 
    rospy.Subscriber("map", OccupancyGrid, callback)
    plt.ion()
    plt.show()
    rospy.spin()

