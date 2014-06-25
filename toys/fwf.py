#!/usr/bin/python
from math import sin,cos,sqrt
import numpy as np
import cv2
import cv2.cv as cv
import sys

global mem

def showhist( hist, bins, w=400, h=400):
    hsz = 32
    hImage = cv.CreateImage( (w, h), cv.IPL_DEPTH_8U, 3 )
    for z in range(0, bins):
        cv.Rectangle( hImage, (z*(w/hsz), z+1*(w/hsz)), ( (z+1)*(w/hsz), hist[z]*h/255), (0,0,255),-1)
    cv.ShowImage( "hist", hImage)

def findlefteye( image, face):
    parent = cv.GetImageROI( image)
    searchROI = (
        face[0],
        face[1]+(face[3]/8),
        face[2]/2,
        int(face[3]*.6))
    findeye( image, searchROI, "Left")
    cv.SetImageROI( image, parent)

def findrighteye( image, face):
    parent = cv.GetImageROI( image)
    searchROI = (
        face[0]+face[2]/2,
        face[1]+(face[3]/8),
        face[2]/2,
        int(face[3]*.6))
    findeye( image, searchROI, "Right")
    cv.SetImageROI( image, parent)

def doface ( image, face):
    parent = cv2.GetImageROI( image)
    cv2.SetImageROI( image, face)
    findlefteye( image, face)
    findrighteye( image, face)
    #
    cv.PyrMeanShiftFiltering( image, image, 15,15)
    cv.SetImageROI( image, parent)

def doalgo( image):
    gray = cv2.cvtColor( image, cv2.COLOR_BGR2GRAY ) 
    cascade = cv2.CascadeClassifier("/usr/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml")
    n = 0
    if( cascade ):
        faces = cascade.detectMultiScale(gray, 1.2, 2, 0, (image.shape[1]/2, image.shape[0]/2))
        for face in faces:
            doface(image, face)
    return image

def doeye( image, eyerect, which):
    parent = cv.GetImageROI( image)
    cv.SetImageROI( image, (eyerect[0]+parent[0],eyerect[1]+parent[1],eyerect[2],eyerect[3]))
    hsv = cv.CreateImage( (eyerect[2], eyerect[3]), cv.IPL_DEPTH_8U, 3 )
    hue = cv.CreateImage( (eyerect[2], eyerect[3]), cv.IPL_DEPTH_8U, 1 )
    cv.CvtColor( image, hsv, cv.CV_BGR2HSV )
    cv.Split( hsv, hue, None, None, None)
    dims = [4]
    ranges = [[0,255]]
    hist = cv.CreateHist( dims, cv.CV_HIST_ARRAY, ranges,1)
    cv.CalcHist( [hue], hist, 1, None)
    showhist(hist, 4)
    cv.PyrMeanShiftFiltering( image, image, 15,15)
    cv.Dilate( image, image, None, 3)
    cv.ShowImage( which+"eye", image )
    cv.SetImageROI( image, parent)

def findeye(image, facehalf, which):
    parent = cv.GetImageROI( image)
    cv.SetImageROI( image, facehalf)
    cv.ShowImage( which, image )
    cascade = cv.Load("/usr/share/OpenCV/haarcascades/haarcascade_eye.xml")
    if( cascade ):
            eyes = cv.HaarDetectObjects(image, cascade, mem, 1.2, 2, cv.CV_HAAR_DO_CANNY_PRUNING, (20,20))
            for (eye),n in eyes:
                doeye( image, eye, which)
    cv.SetImageROI( image, parent)



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
            cv2.imshow( "Camera", image )
            wait = 1
            algoimage=doalgo( image)
            if( algoimage.all == False ):
                cv2.imshow( "Algo", algoimage )
                del algoimage
                wait = 10000
            if( cv2.waitKey(wait) == 27 ):
                break
            del image
    cv2.destroyWindow( "Camera" )
    cv2.destroyWindow( "Algo" )
# vi:ai:ts=4:sw=4:et:syntax:
