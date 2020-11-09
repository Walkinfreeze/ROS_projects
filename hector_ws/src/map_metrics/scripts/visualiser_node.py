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
from scipy.io import savemat
from nav_msgs.msg import *
from std_msgs.msg import Float64
import datetime
import shutil

datetime_object = datetime.datetime.now()
np.set_printoptions(threshold=np.inf)

target_path = os.path.join(os.path.dirname(__file__), '../figures')
my_path=os.path.normpath(target_path)

target_path1 = os.path.join(os.path.dirname(__file__), '../figures/'+str(datetime_object))
my_path1=os.path.normpath(target_path1)
os.mkdir(my_path1)

target_path2 = os.path.join(os.path.dirname(__file__), '../matfiles')
my_path2=os.path.normpath(target_path2)

txt_file = str(datetime_object)+'.mat'
class Visualiser:
    def __init__(self):
        self.fig, self.ax=plt.subplots()
        self.ln, = plt.plot([],[],'ro')
        self.fig.suptitle('Occupied Surface / time')
        self.ax.set_ylabel('Occupied Surface [m]')
        self.ax.set_xlabel('time')
        self.ax.grid()
        self.x_data, self.y_data= [], []
	self.erase_ = []
	self.time = 0
        self.time0 = rospy.get_rostime().to_sec()


    def plot_init(self):
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        return self.ln

    def callback(self, data1):
        map_quality_ = data1.data
        self.time1 = rospy.get_rostime().to_sec()
        self.time = self.time1-self.time0

        self.y_data.append(map_quality_)	
       # x_index = len(self.x_data)
        self.x_data.append(self.time)
        diff = np.diff(self.y_data)
        savemat(os.path.join(my_path2, txt_file), mdict={'x_data':self.x_data,'y_data': self.y_data, 'diff':diff,'erased_data': self.erase_})

    def callback_map(self, data2):
        bin_map_= data2.data
        binary_map_ = np.array(data2.data).reshape(data2.info.height, data2.info.width)
        datetime_object1 = datetime.datetime.now()
        my_file_map = str(self.time) +'_map'+'.png'
        plt.imsave(os.path.join(my_path1, my_file_map), binary_map_, cmap="gray")

    def callback_erase(self,data3):
	self.erase_.append(data3.data)

    def update_plot(self, frame):
        self.ln.set_data(self.x_data,self.y_data)
        self.ax.relim()
        self.ax.autoscale() 
        plt.draw()
        return self.ln

rospy.init_node('listener', anonymous=True)
vis= Visualiser()
sub1=rospy.Subscriber("map_erased", Float64 , vis.callback_erase)
sub2=rospy.Subscriber("map_quality", Float64 , vis.callback)
sub3=rospy.Subscriber("binary_map", OccupancyGrid, vis.callback_map) 
ani = FuncAnimation(vis.fig, vis.update_plot) #init_func=vis.plot_init

plt.show(block=True) 
rospy.spin()     

