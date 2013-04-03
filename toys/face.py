#!/usr/bin/python
from math import sin,cos,sqrt
import cv2.cv as cv
import sys

def doalgo( image):
    #create an appropriate sized image and set ut to the input image
    newimage = cv.CreateMat(image.height, image.width, cv.CV_8UC3)
    cv.Resize( image, newimage)

    storage = cv.CreateMemStorage()
    haar=cv.Load('haarcascade_frontalface_default.xml')
    faces = cv.HaarDetectObjects(newimage, haar, storage, 1.2, 2,cv.CV_HAAR_DO_CANNY_PRUNING, (100,100))
    if faces:
        for (x,y,w,h),n in faces:
            cv.Rectangle(newimage, (x,y), (x+w,y+h), 255)
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
# vi:ai:ts=4:sw=4:et:syntax:
