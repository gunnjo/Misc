#!/usr/bin/python
import cv2
import sys
import numpy as np

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))

def scaleshow( win, image):
    width = image.shape[1]
    height = image.shape[0]
    if ( width > 800 or height > 600 ):
       width = 800
       height = 600
    i = cv2.resize( image, (width, height), 0, 0, cv2.INTER_NEAREST)
    cv2.imshow( win, i )

def filterContour( contour):
    minArea = 2.75*1.25 # minimum area in inches
    ppi = 200.
    epsilon = 0.1*cv2.arcLength(contour,True)
    approx = cv2.approxPolyDP(contour,epsilon,True)
    if ( len(approx) != 4  ): #only square objects
        return None
    if ( cv2.isContourConvex(approx) is False ): #That are closed
        return None
    area = cv2.contourArea(approx)
    if area < (minArea*ppi*.9): #only large enough objects
        return None
    return(approx)

def doalgo( image, model):
    fgmask = model.apply(image)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    gray = image[:,:,1]    
    ret, edges = cv2.threshold(gray, 170, 255,0)
    contours, hierarchy = cv2.findContours( edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    interestingContours = []
    for contour in contours:
        adjustedContour = filterContour(contour)
        if adjustedContour is not None:
            interestingContours.append(adjustedContour)
    cv2.drawContours(fgmask, interestingContours, -1, 255, 3)
    return fgmask

if __name__ == "__main__":
    capture = None

    if len(sys.argv)==1:
        capture = cv2.VideoCapture( 0 )
    elif len(sys.argv)==2 and sys.argv[1].isdigit():
        capture = cv2.VideoCapture( int(sys.argv[1]) )
    elif len(sys.argv)==2:
        capture =cv2.VideoCapture( sys.argv[1] ) 

    if not capture:
        print "Could not initialize capturing..."
        sys.exit(-1)
        
    cv2.namedWindow( "Camera", 1 )
    cv2.namedWindow( "Algo", 1 )

    model = cv2.BackgroundSubtractorMOG()
    for i in range(10):
        ret, image = capture.read( )
        fgmask = model.apply(image)
    while True:
        if ( capture and capture.isOpened() ):
            ret, image = capture.read( )
            if( ret ):
                scaleshow( "Camera", image )
                algoimage=doalgo( image, model)
                if( algoimage is not None):
                    scaleshow( "Algo", algoimage )
                    del algoimage
                del image
        if( cv2.waitKey(10) == 27 ):
            break
    cv2.destroyWindow( "Camera" )
    cv2.destroyWindow( "Algo" )
# vi:ai:ts=4:sw=4:et:syntax: