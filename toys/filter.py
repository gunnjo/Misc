#!/usr/bin/python
from math import sin,cos,sqrt
import sys, subprocess
import os.path
import numpy as np
import cv2
import cv2.cv as cv

global mem
DEFAULT_THRESHOLD = 32

def nothing(*arg, **kw):
    pass

def doalgo( image):
    thrs = cv2.getTrackbarPos('threshold', 'filter')
    t = cv2.cvtColor( image, cv.CV_BayerBG2RGB )
    g = t[:,:,1]
    ret, edges = cv2.threshold(g, thrs, 255,0)

    scaleshow("thresh", edges)    

    return t

def scaleshow( win, image):
    width = image.shape[1]
    height = image.shape[0]
    if ( width > 800 or height > 600 ):
       width = 800
       height = 600
    i = cv2.resize( image, (width, height), 0, 0, cv2.INTER_NEAREST)
    cv2.imshow( win, i )

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
    cv2.namedWindow('filter')    

    cv2.createTrackbar('threshold', 'filter', DEFAULT_THRESHOLD, 255, nothing)

    while True:
        if ( capture and capture.isOpened() ):
            ret, image = capture.read( )
        else:
            image = cv2.imread( sys.argv[1], 0 )
            ret = image is not None 

        if( ret ):
            wait = 1
            algoimage=doalgo( image)
            scaleshow( "Camera", image )
            if( algoimage.any() ):
                scaleshow( "Algo", algoimage )
                del algoimage
                wait = 1000
            if( cv2.waitKey(wait) == 27 ):
                break
            del image
    cv2.destroyWindow( "Camera" )
    cv2.destroyWindow( "Algo" )
# vi:ai:ts=4:sw=4:et:syntax:
