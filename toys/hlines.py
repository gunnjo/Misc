#!/usr/bin/python
from math import sin,cos,sqrt
import cv2.cv as cv
import sys

def doalgo( image):
    #create an appropriate sized image and set ut to the input image
    newimage = cv.CreateMat(image.height, image.width, cv.CV_8UC3)
    cv.Resize( image, newimage)
    hlsimage = cv.CreateMat(image.height, image.width, cv.CV_8UC3)
    cv.Resize( newimage, hlsimage)
    #channel images
    c1image = cv.CreateImage( cv.GetSize(newimage), 8, 1 )
    cv.CvtColor(newimage,hlsimage, cv.CV_BGR2HLS)
    channels = [ None, None, None ]
    channels[0] = c1image
    cv.Split( newimage, channels[0], channels[1], channels[2], None)
    mem = cv.CreateMemStorage(0)
    lines = 0
    cv.Canny( c1image, c1image, 50, 200, 3)
    lines = cv.HoughLines2( c1image, mem, cv.CV_HOUGH_PROBABILISTIC, 1, cv.CV_PI/180, 50, 50, 10 )

    for i in range(min(len(lines), 100)):
        line = lines[i]
        cv.Line( newimage, line[0], line[1], cv.CV_RGB(255,0,0), 3, 8 )

    del mem;
    del c1image;
    return newimage

if __name__ == "__main__":
    capture = 0

    if len(sys.argv)==1:
        capture = cv.CaptureFromCAM( 0 )
    elif len(sys.argv)==2 and sys.argv[1].isdigit():
        capture = cv.CaptureFromCAM( int(sys.argv[1]) )
    elif len(sys.argv)==2:
        capture = cv.CaptureFromCAM( sys.argv[1] ) 

    if not capture:
        print "Could not initialize capturing..."
        sys.exit(-1)
        
    cv.NamedWindow( "Camera", 1 )
    cv.NamedWindow( "Algo", 1 )
    while True:

        if(cv.GrabFrame( capture ) ):
            image = cv.RetrieveFrame( capture )
        if( image ):
            cv.ShowImage( "Camera", image )
            algoimage=doalgo( image)
            if( algoimage ):
                cv.ShowImage( "Algo", algoimage )
                del algoimage
            del image
        if( cv.WaitKey(10) != -1 ):
            break
    cv.DestroyWindow( "Camera" )
    cv.DestroyWindow( "Algo" )
