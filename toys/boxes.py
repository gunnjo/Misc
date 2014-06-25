#!/usr/bin/python
from math import sin,cos,sqrt
import sys
import numpy as np
import cv2
import cv2.cv as cv

global mem

def doalgo( image):
    gray = cv2.cvtColor( image, cv2.COLOR_BGR2GRAY )
    corners = cv2.goodFeaturesToTrack( gray, 8, .1, 10 )
    corners = np.int0(corners)
    print "Trying ", len(corners)

    for corner in corners:
        x,y = corner.ravel()
        print "x=", x,  " y=", y
        cv2.circle( image, (x,y), 10, (255, 0, 0), -1)

    return gray

if __name__ == "__main__":
    capture = None 
    image = None 

    if len(sys.argv)==1:
        capture = cv2.VideoCapture( 0 )
    elif len(sys.argv)==2 and sys.argv[1].isdigit():
        capture = cv2.VideoCapture( int(sys.argv[1]) )
    elif len(sys.argv)==2:
        image = cv2.imread( sys.argv[1] ) 

    if not capture.isOpened() and (image is None):
        print "Could not initialize capturing..."
        sys.exit(-1)
        
    cv2.namedWindow( "Camera", 1 )
    cv2.namedWindow( "Algo", 1 )

    while True:
        if ( capture.isOpened() ):
            ret, image = capture.read( )
        else:
            ret, image = cv2.imread( sys.argv[1] ) 

        if( ret ):
            wait = 1
            algoimage=doalgo( image)
            cv2.imshow( "Camera", image )
            if( algoimage.any() ):
                cv2.imshow( "Algo", algoimage )
                del algoimage
                wait = 1000
            if( cv2.waitKey(wait) == 27 ):
                break
            del image
    cv2.destroyWindow( "Camera" )
    cv2.destroyWindow( "Algo" )
# vi:ai:ts=4:sw=4:et:syntax:
