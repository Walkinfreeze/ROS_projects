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

resolution = 0.05

numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

datetime_object = datetime.datetime.now()
np.set_printoptions(threshold=np.inf)

target_path = os.path.join(os.path.dirname(__file__), '../figures/')
my_path=os.path.normpath(target_path)

target_path1 = os.path.join(os.path.dirname(__file__), '../figures/2020-11-04 10:45:33.568604')
my_path1=os.path.normpath(target_path1)

target_path2 = os.path.join(os.path.dirname(__file__), '../matfiles')
my_path2=os.path.normpath(target_path2)

# extracting file names with extensions
full_file_names=[f for f in listdir(my_path1) if f.endswith('.png')]
full_file_names=sorted(full_file_names, key=numericalSort)

# Python program to illustrate 
# template matching 
import cv2 
import numpy as np 

pt_array = []
erase_array = []

for i in range(len(full_file_names)-1):
	# Read the main image 
	img_rgb = cv2.imread(my_path1+'/'+full_file_names[i+1],0)

# Convert it to grayscale 
	#img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY) 

	# Read the template 
	template = cv2.imread(my_path1+'/'+full_file_names[i],0)
	print(full_file_names[i]) 	

	if img_rgb.shape >= template.shape:
		# Store width and height of template in w and h 
		w, h = template.shape[::-1] 

		# Perform match operations. 
		res = cv2.matchTemplate(img_rgb,template,cv2.TM_CCOEFF_NORMED) 


		# Specify a threshold 
		threshold = 0.1

		# Store the coordinates of matched area in a numpy array 
		loc = np.where( res >= threshold) 

		# Draw a rectangle around the matched region. 
		for pt in zip(*loc[::-1]):
			h = h
			#cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 1) 
		erase_ = 0
		for j in range(template.shape[0]):
			for k in range(template.shape[1]):
                		a = int(img_rgb[j+pt[1],k+pt[0]])
                		b = int(template[j,k])			
          			if (a-b) == 255:
					erase_ += 1
		print("case 1")
		erase_array.append(erase_*resolution)
		print(erase_array)
	
	else:
		template_ = img_rgb
		current_ = template
		# Store width and height of template in w and h 
		w, h = template_.shape[::-1] 

		# Perform match operations. 
		res = cv2.matchTemplate(current_,template_,cv2.TM_CCOEFF_NORMED) 


		# Specify a threshold 
		threshold = 0.1

		# Store the coordinates of matched area in a numpy array 
		loc = np.where( res >= threshold) 

		# Draw a rectangle around the matched region. 
		for pt in zip(*loc[::-1]):
			h = h
			#cv2.rectangle(current_, pt, (pt[0] + w, pt[1] + h), (0,0,255), 1) 
	
		for j in range(template_.shape[0]):
			for k in range(template_.shape[1]):
                		a = int(current_[j+pt[1],k+pt[0]])
                		b = int(template_[j,k])				
          			if (a-b) == -255:
					erase_ += 1
		print("case_2")
		erase_array.append(erase_*resolution)
		print(erase_array)
		# Show the final image with the matched area. 
	cv2.imshow('Detected',img_rgb) 
	cv2.waitKey(0)	

