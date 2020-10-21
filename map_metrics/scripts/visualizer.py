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
from matplotlib.animation import FuncAnimation

from nav_msgs.msg import *
import datetime
import shutil

datetime_object = datetime.datetime.now()
np.set_printoptions(threshold=np.inf)


my_path = os.path.normpath(os.getcwd() + os.sep + os.pardir+'/'+'hector_ws'+'/'+'src'+'/'+'map_metrics'+'/'+'figures')

os.mkdir(os.path.normpath(os.getcwd() + os.sep + os.pardir+'/'+'hector_ws'+'/'+'src'+'/'+'map_metrics'+'/'+'figures'+'/'+str(datetime_object)))
my_path1 = os.path.normpath(os.getcwd() + os.sep + os.pardir+'/'+'hector_ws'+'/'+'src'+'/'+'map_metrics'+'/'+'figures'+'/'+str(datetime_object))

class Visualiser:
    def __init__(self):
        self.fig, self.ax=plt.subplots()
        self.ln, = plt.plot([],[],'ro')
        self.x_data, self.y_data= [], []

    def plot_init(self):
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        return self.ln

    def callback(self, data):
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
        
        self.y_data.append(occupied_)
        x_index = len(self.x_data)
        self.x_data.append(x_index+1)
        print(self.y_data)

    def update_plot(self, frame):
        self.ln.set_data(self.x_data,self.y_data)
        self.ax.relim()
        self.ax.autoscale() 
        plt.draw()
        return self.ln

rospy.init_node('listener', anonymous=True) 
vis= Visualiser()
rospy.Subscriber("map", OccupancyGrid, vis.callback)
ani = FuncAnimation(vis.fig, vis.update_plot) #init_func=vis.plot_init

plt.show(block=True) 
rospy.spin()     

