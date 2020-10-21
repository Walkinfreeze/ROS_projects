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

occupied_vector_ = []
occupied_surface_vector_ = []
free_vector_ = []
free_surface_vector_ = []

my_path = os.path.normpath(os.getcwd() + os.sep + os.pardir+'/'+'hector_ws'+'/'+'src'+'/'+'map_metrics'+'/'+'figures')

os.mkdir(os.path.normpath(os.getcwd() + os.sep + os.pardir+'/'+'hector_ws'+'/'+'src'+'/'+'map_metrics'+'/'+'figures'+'/'+str(datetime_object)))
my_path1 = os.path.normpath(os.getcwd() + os.sep + os.pardir+'/'+'hector_ws'+'/'+'src'+'/'+'map_metrics'+'/'+'figures'+'/'+str(datetime_object))


def callback(data):
    map_data = data
    map_ = np.array(map_data.data).reshape(map_data.info.height, map_data.info.width)
    print(map_.shape)
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
    occupied_surface_ = occupied_ * map_data.info.resolution 
    free_surface_ = free_ * map_data.info.resolution    
    occupied_vector_.append(occupied_)
    free_vector_.append(free_)
    occupied_surface_vector_.append(occupied_surface_)
    free_surface_vector_.append(free_surface_)

    # x axis values 
    x_ = range(len(free_vector_)) 
    # corresponding y axis values 
    y_occupied_ = occupied_vector_
    y_free_ = free_vector_

    fig, (ax1, ax2) = plt.subplots(2, 1)
    fig.suptitle('Amount of Pixels Occupied/Free')
    ax1.plot(x_, y_occupied_, 'r', marker='.') 
    ax1.set_ylabel('occupied pixels')
    ax1.set_xlabel('map_files')
    ax1.grid() 
    ax2.plot(x_, y_free_, 'g', marker='.')
    ax2.set_xlabel('map files')
    ax2.set_ylabel('free pixels')
    ax2.grid()

    my_file_fig = str(datetime_object)+'_fig' +'.png'
    fig.savefig(os.path.join(my_path, my_file_fig))
    plt.close()

    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    X = np.arange(len(free_vector_))

    plt.bar(X, occupied_surface_vector_, align='center')
    plt.ylabel('Occupied Length [m]')
    plt.title('Occupied Length Diagram')

    my_file_bar = str(datetime_object) + '_bar'+'.png'
    plt.savefig(os.path.join(my_path, my_file_bar)) 
    plt.close()

    datetime_object1 = datetime.datetime.now()
    my_file_map = str(datetime_object1) +'_map'+'.png'
    plt.imsave(os.path.join(my_path1, my_file_map), map_, cmap="gray")
    plt.close()
    
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("map", OccupancyGrid, callback)


    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()

