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
from std_msgs.msg import Float64
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
        self.fig.suptitle('Occupied Surface / times listened')
        self.ax.set_ylabel('Occupied Surface [m]')
        self.ax.set_xlabel('index')
        self.x_data, self.y_data= [], []

    def plot_init(self):
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        return self.ln

    def callback(self, data1):
        map_quality_ = data1.data

        self.y_data.append(map_quality_)
        x_index = len(self.x_data)
        self.x_data.append(x_index)

    def callback_map(self, data2):
        bin_map_= data2.data
        binary_map_ = np.array(data2.data).reshape(data2.info.height, data2.info.width)
        datetime_object1 = datetime.datetime.now()
        my_file_map = str(datetime_object1) +'_map'+'.png'
        plt.imsave(os.path.join(my_path1, my_file_map), binary_map_, cmap="gray")

    def update_plot(self, frame):
        self.ln.set_data(self.x_data,self.y_data)
        self.ax.relim()
        self.ax.autoscale() 
        plt.draw()
        return self.ln

vis= Visualiser()
rospy.init_node('listener', anonymous=True)
sub1=rospy.Subscriber("binary_map", OccupancyGrid, vis.callback_map) 
sub2=rospy.Subscriber("map_quality", Float64 , vis.callback)
ani = FuncAnimation(vis.fig, vis.update_plot) #init_func=vis.plot_init

plt.show(block=True) 
rospy.spin()     

