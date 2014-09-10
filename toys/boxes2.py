#!/usr/bin/python
from math import sin,cos,sqrt,pi
import sys, subprocess
import os.path
import numpy as np
import cv2
import cv2.cv as cv
import zbar

global mem

def ocrContour(image):
    lines = []
    wdir = "."
    base = "%d-%d" %image.shape
    ifile = "%s/image_%s.tif" %(wdir,base)
    tbase = "%s/text_%s" %(wdir, base)
    otext = "%s.txt" %tbase
    cmd = "tesseract %s %s" % (ifile, tbase)
    cv2.imwrite(ifile, image)
    print cmd
    subprocess.call([cmd], shell=True, stderr=subprocess.PIPE)
    if ( os.path.exists( otext) is True ):
	lines.append( [l.strip() for l in open(otext).readlines()])
    image = cv2.flip(image,-1)
    ifile = "%s/image_flip_%s.tif" %(wdir,base)
    tbase = "%s/text_flip_%s" %(wdir, base)
    otext = "%s.txt" %tbase
    cv2.imwrite(ifile, image)
    cmd = "tesseract %s %s" % (ifile, tbase)
    subprocess.call([cmd], shell=True, stderr=subprocess.PIPE)
    print cmd
    if ( os.path.exists( otext) is True ):
        lines.append([l.strip() for l in open(otext).readlines()])
    if (lines):
        return lines[0]
    else:
        return None

def processContour( contour, gray, contours):
    rr = cv2.minAreaRect(contour)
    m = cv2.moments(contour)
    print "Rotated:", rr
    rmat = cv2.getRotationMatrix2D( rr[0], rr[2], 1.0)
    rgray = gray#[rr[0][1]-(rr[1][1]/2):rr[0][1]+(rr[1][1]/2),rr[0][0]-(rr[1][0]/2):rr[0][0]+(rr[1][0]/2)]
    rimg = cv2.warpAffine(rgray, rmat, rgray.shape[0:2], flags=cv2.INTER_CUBIC)
    rimg = rimg[rr[0][0]-(rr[1][0]/2):rr[0][0]+(rr[1][0]/2),rr[0][1]-(rr[1][1]/2):rr[0][1]+(rr[1][1]/2)]
    print "shape: ",rimg.shape
    if ( (rimg.shape[0] is 0) or (rimg.shape[1] is 0) ):
        print "empty shape"
    else:
        cv2.imshow("rotated", rimg)
        scanner = zbar.ImageScanner()
        scanimg = zbar.Image(rimg.shape[1], rimg.shape[0], 'Y800', rimg.tostring() )
        scanner.scan(scanimg)
        for code in scanimg:
            print "code:", code.type, " contents:", '"%s"' % code.data
        ocrContour(rimg)
    return None

def filterContour( i, contours, hierarchy, image):
    minArea = 2.75*1.25 # minimum area in inches
    ppi = 400.
    epsilon = 0.1*cv2.arcLength(contours[i],True)
    approx = cv2.approxPolyDP(contours[i],epsilon,True)
#    approx = cv2.convexHull(contours[i],None,True, True)
#    if ( abs(cv2.contourArea(approx) - cv2.contourArea(contours[i])) > ppi*minArea ):
#        cv2.imwrite("test%d.tif"%i, image)
#        print "approx: ", approx, " orig: ", contours[i]
    if hierarchy[i][2] == -1 : #only parent objects
        cv2.drawContours(image, contours[i], -1, (0,75,255), 3)
        return None
    scaleshow("approx", image)        
#    if ( len(approx) != 4  ): #only square objects
#        cv2.drawContours(image, contours[i], -1, (0,150,255), 3)
#        return None
#    if ( cv2.isContourConvex(approx) is False ): #That are closed
#        cv2.drawContours(image, contours[i], -1, (0,225,255), 3)
#        return None
    area = cv2.contourArea(contours[i])
    if (area/ppi) < (minArea*0.9): #only large enough objects
        cv2.drawContours(image, contours[i], -1, (0,255,255), 3)
        return None
    print "Approx!: ", approx
    return(approx)

def scaleshow( win, image):
    width = image.shape[1]
    height = image.shape[0]
    if ( width > 800 or height > 600 ):
       width = 800
       height = 600
    i = cv2.resize( image, (width, height), 0, 0, cv2.INTER_NEAREST)
    cv2.imshow( win, i )

def doalgo( image):
    #hsv = cv2.cvtColor( image, cv2.COLOR_BGR2HSV)
    #gray = hsv[:,:,2]
    gray = image[:,:,1]
#    gray = cv2.GaussianBlur(gray, (5, 5), 0)    
    ret, edges = cv2.threshold(gray,190, 255,0)
    contours, hierarchy = cv2.findContours( edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(image, contours, -1, (0,0,0), 3)
    interestingContours = []
    interestingContoursIndex = []
    for i in xrange(len(contours)):
        adjustedContour = filterContour(i, contours, hierarchy[0], image)
        if adjustedContour is not None:
            interestingContours.append(adjustedContour)
            interestingContoursIndex.append(i)
    subcontours = []
    i = 0
    for contour in interestingContours:
        processContour(contour, gray, contours)
        i=i+1
    cv2.drawContours(image, interestingContours, -1, (255,0,0), 3)
    scaleshow("interesting", image)
    cv2.imwrite("interesting%d.tif"%i, image)
    return edges

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

    while True:
        if ( capture and capture.isOpened() ):
            ret, image = capture.read( )
        else:
            image = cv2.imread( sys.argv[1] )
            ret = image is not None 

        if( ret ):
            wait = 1
            algoimage=doalgo( image)
            scaleshow( "Camera", image )
            if( algoimage is not None ):
                scaleshow( "Algo", algoimage )
                del algoimage
            if ( capture is None):
                wait = 0
            if( cv2.waitKey(wait) == 27 ):
                break
            del image
    cv2.destroyWindow( "Camera" )
    cv2.destroyWindow( "Algo" )
# vi:ai:ts=4:sw=4:et:syntax:
