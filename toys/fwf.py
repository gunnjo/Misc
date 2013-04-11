#!/usr/bin/python
from math import sin,cos,sqrt
import cv2
import cv2.cv as cv
import sys

global mem

def eyes ( image, face):
    print "working on", face
    eye( image, (face[0], face[1], face[2]/2, face[3]/2))
    eye( image, (face[0]+face[2]/2, face[1]+face[3]/2, face[2]/2, face[3]/2))

def eye(image, facehalf):
    cv.SetImageROI( image, facehalf)
    cascade = cv.Load("/usr/share/OpenCV/haarcascades/haarcascade_eye.xml")
    if( cascade ):
            eyes = cv.HaarDetectObjects(image, cascade, mem, 1.2, 2, cv.CV_HAAR_DO_CANNY_PRUNING, (20,20))
            for (eye),n in eyes:
                print "\teye at", eye
                cv.SetImageROI( image, eye)
                cv.Rectangle( image, (eye[0], eye[1]), (eye[2], eye[3]), (0,255,0),-1)
                cv.Dilate( image, image, None, 3)
    cv.SetImageROI( image, (0,0,image.width,image.height))

def doalgo( image):
    storage = cv.CreateMemStorage(0)
    #cv.ClearMemStorage(storage)
    #create an appropriate sized image and set ut to the input image
    newimage = cv.CreateImage((image.width, image.height), 8, 3)
    cv.Resize( image, newimage)
    #cv.CvtColor( image, newimage, cv.CV_BGR2GRAY)
    cascade = cv.Load("/usr/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml")

    if( cascade ):
            faces = cv.HaarDetectObjects(newimage, cascade, mem, 1.2, 2, cv.CV_HAAR_DO_CANNY_PRUNING, (image.height/3, image.width/3))
            for (face),n in faces:
                eyes(newimage, face)
    #contours = cv.FindContours( newimage, storage, cv.CV_RETR_TREE, cv.CV_CHAIN_APPROX_SIMPLE)

    #newimage = cv.CreateMat(image.height, image.width, cv.CV_8UC3)
    #print len(contours)
    #cv.DrawContours( newimage, contours,(255,0,0), (0,255,0), 0)

    return newimage

if __name__ == "__main__":
    mem = cv.CreateMemStorage(0);
    capture = None 
    image = None 

    if len(sys.argv)==1:
        capture = cv.CaptureFromCAM( 0 )
    elif len(sys.argv)==2 and sys.argv[1].isdigit():
        capture = cv.CaptureFromCAM( int(sys.argv[1]) )
    elif len(sys.argv)==2:
        image = cv.LoadImage( sys.argv[1] ) 

	print type(image)
    if not capture and not image:
        print "Could not initialize capturing..."
        sys.exit(-1)
        
    cv.NamedWindow( "Camera", 1 )
    cv.NamedWindow( "Algo", 1 )
    while True:

	if ( not capture == None ):
		if(cv.GrabFrame( capture ) ):
		    image = cv.RetrieveFrame( capture )
	else:
		image = cv.LoadImage( sys.argv[1] ) 
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
