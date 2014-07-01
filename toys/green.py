#!/usr/bin/python
from math import sin,cos,sqrt
import sys
import numpy as np
import cv2
import cv2.cv as cv

global mem

def doalgo( image):
    return image[:,:,1]

if __name__ == "__main__":
    capture = None 
    image = None 

    if len(sys.argv)==1:
        capture = cv2.VideoCapture( 0 )
    elif len(sys.argv)==2 and sys.argv[1].isdigit():
        capture = cv2.VideoCapture( int(sys.argv[1]) )
    elif len(sys.argv)==2:
        image = cv2.imread( sys.argv[1] ) 

    if  (image is None) and not capture.isOpened():
        print "Could not initialize capturing..."
        sys.exit(-1)
       
    cv2.namedWindow( "Camera", 1 )
    cv2.namedWindow( "Algo", 1 )

    c = 1
    if ( capture and capture.isOpened() ):
       ret, image = capture.read( )
    else:
       image = cv2.imread( sys.argv[1] )
       ret = image is not None 

    if( ret ):
       algoimage=doalgo( image)
       cv2.imwrite("green.png", algoimage)
       del image
    cv2.destroyWindow( "Camera" )
    cv2.destroyWindow( "Algo" )
# vi:ai:ts=4:sw=4:et:syntax:
