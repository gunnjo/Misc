#!/usr/bin/python
import cv2
import sys
import numpy as np

def cf32show( win, image, n):
    ni = cv2.convertScaleAbs(image/n)
    scaleshow( win, ni)

def scaleshow( win, image):
    width = image.shape[1]
    height = image.shape[0]
    if ( width > 800 or height > 600 ):
       width = 800
       height = 600
    i = cv2.resize( image, (width, height), 0, 0, cv2.INTER_NEAREST)
    cv2.imshow( win, i )

accimage = None


def doalgo( image):
        cv2.accumulate( image, accimage)
        return accimage

if __name__ == "__main__":
    capture = None 
    image = None
    n = 0 

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

    while True:
        if ( capture and capture.isOpened() ):
            ret, image = capture.read( )
        else:
            image = cv2.imread( sys.argv[1] )
            ret = image is not None 

        if( ret ):
            n+=1
            wait = 1
            if accimage == None:
                accimage = np.zeros(image.shape, np.float32)
            algoimage=doalgo( image)
            scaleshow( "Camera", image )
            if( algoimage is not None ):
                cf32show( "Algo", algoimage, n )
                del algoimage
                wait = 1000
            if( cv2.waitKey(wait) == 27 ):
                break
            del image
    cv2.destroyWindow( "Camera" )
    cv2.destroyWindow( "Algo" )
# vi:ai:ts=4:sw=4:et:syntax:
