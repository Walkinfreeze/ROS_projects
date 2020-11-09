#!/usr/bin/env python
import re
import numpy as np
import rospy
    
# license removed for brevity
from std_msgs.msg import Float64
from nav_msgs.msg import *

np.set_printoptions(threshold=np.inf)

class Process:
	def init(self):
		self.count_= 0

	def callback(self,data):
		self.map_data_ = data
		self.map_current_ = np.array(self.map_data_.data).reshape(self.map_data_.info.height,self.map_data_.info.width)

    		self.free_ = 0
    		self.occupied_ = 0
		self.erase_ = 0		
		for i in range(self.map_current_.shape[0]):
		       for j in range(self.map_current_.shape[1]):
          			if self.map_current_[i,j] > 60:
                  			self.occupied_ += 1
                  			self.map_current_[i,j]=0 # 0 is black
          			else:
                  			self.free_ += 1
                  			self.map_current_[i,j]=1 # 1 is white
		grid = OccupancyGrid()
    		grid.data = self.map_current_.ravel()
    		grid.info = MapMetaData()
    		grid.info.height = self.map_current_.shape[0]
    		grid.info.width = self.map_current_.shape[1]

    		pub1 = rospy.Publisher('binary_map', OccupancyGrid, queue_size=1)
    		pub1.publish(grid)

		occupied_surface_ = self.occupied_ * self.map_data_.info.resolution

    		pub2 = rospy.Publisher('map_quality', Float64, queue_size=1)
    		pub2.publish(occupied_surface_)
		
		if self.count_ == 0:
			self.map_previous_ = self.map_current_

   		for i in range(self.map_current_.shape[0]):
       			for j in range(self.map_current_.shape[1]):
          			if (self.map_current_[i,j]-self.map_previous_[i,j]) == 1:
					self.erase_ += 1


		erased_surface = self.erase_ * self.map_data_.info.resolution

    		pub3 = rospy.Publisher('map_erased', Float64, queue_size=1)
    		pub3.publish(erased_surface)

		proc.set_previous()
		self.count_ +=1

		
	def set_previous(self):
		self.map_previous_ = self.map_current_
proc=Process()
proc.init()		
rospy.init_node('listener', anonymous=True)
rospy.Subscriber("map", OccupancyGrid, proc.callback)
rospy.spin()

