#!/usr/bin/python
from math import sin,cos,sqrt,pi
import sys, subprocess
import os.path
from os import listdir
from os.path import isfile, join
import numpy as np
import cv2
import re

def scaleshow( win, image):
    width = image.shape[1]
    height = image.shape[0]
    if ( width > 800 or height > 600 ):
       width = 800
       height = 600
    i = cv2.resize( image, (width, height), 0, 0, cv2.INTER_NEAREST)
    cv2.imshow( win, i )

if __name__ == "__main__":
    fact_x = 2
    fact_y = 2
    image = None
    path = "x.tiff"

    if len(sys.argv)>1:
        path = sys.argv[1]

    if len(sys.argv)>2:
        fact_x = int(sys.argv[2])
        fact_y = fact_x

    if len(sys.argv)>3:
        fact_y = int(sys.argv[3])
        
    cv2.namedWindow( "Camera", 1 )

    if ( isfile( path ) ):
        image = cv2.imread( path)
        if (image is not None): 
            scaleshow( "Camera", image )
            k = cv2.waitKey(0)
            i = cv2.resize( image, (0,0), fx=1.0/fact_x,fy = 1.0/fact_y, interpolation=cv2.INTER_NEAREST)
            base,_ = os.path.splitext(path) 
            n = base + "_downscale_x_" + str(fact_x) + "_y_" + str(fact_y) + ".tiff"
            cv2.imwrite( n, i )
            print "Image ", n, " is ", k
        else:
            print "could not open '", path, "'"
            lines = []


    cv2.destroyWindow( "Camera" )
# vi:ai:ts=4:sw=4:et:syntax:
