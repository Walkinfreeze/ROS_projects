#!/usr/bin/env python
import re
import numpy

import os
from os import listdir
from os.path import isfile,join
import csv
import sys

numpy.set_printoptions(threshold=1000)


#assign working directory to variable
file_path=os.getcwd()
print(file_path)
#setting path for data folder
data_path=file_path

# extracting file names with extensions
full_file_names=[f for f in listdir(data_path) if f.endswith('.pgm')]

#checking file names and extensions
print(full_file_names)

def read_pgm(filename, byteorder='>'):
    """Return image data from a raw PGM file as numpy array.

    Format specification: http://netpbm.sourceforge.net/doc/pgm.html

    """
    with open(filename, 'rb') as f:
        buffer = f.read()
    try:
        header, width, height, maxval = re.search(
            b"(^P5\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n]\s)*)", buffer).groups()
    except AttributeError:
        raise ValueError("Not a raw PGM file: '%s'" % filename)
    return numpy.frombuffer(buffer,
                            dtype='u1' if int(maxval) < 256 else byteorder+'u2',
                            count=int(width)*int(height),
                            offset=len(header)
                            ).reshape((int(height), int(width)))


if __name__ == "__main__":
    from matplotlib import pyplot
    for k in range(len(full_file_names)):
        image = read_pgm(full_file_names[k], byteorder='<')
        image.setflags(write=1)
        occupied_ = 0
        free_ = 0
        for i in range(image.shape[0]):
           for j in range(image.shape[1]):
              if image[i,j] == 0:
                  image[i,j]=0
                  occupied_ += 1
              else:
                 image[i,j]=1
                 free_  += 1
        print(occupied_)
        print(free_)
        pyplot.imshow(image, pyplot.cm.gray)
        pyplot.show()

