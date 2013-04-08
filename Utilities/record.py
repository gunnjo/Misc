#!/usr/bin/env python
import cv2 as cv
import sys

writer = None
frame_num = 0

def doalgo( image):
	global writer, frame_num
	if (writer == None):
		writer = cv.VideoWriter("test.avi", cv.cv.CV_FOURCC('F','F','V','1'), 30, (image.shape[1],image.shape[0]))
	writer.write(image)
	frame_num+=1
	if ( (frame_num % 10) == 0) :
		print "Frame ",frame_num
        return None

if __name__ == "__main__":
    capture = 0

    if len(sys.argv)==1:
        capture = cv.VideoCapture( 0 )
    elif len(sys.argv)==2 and sys.argv[1].isdigit():
        capture = cv.VideoCapture( int(sys.argv[1]) )
    elif len(sys.argv)==2:
        capture = cv.VideoCapture( sys.argv[1] ) 

    if not capture:
        print "Could not initialize capturing..."
        sys.exit(-1)
        
    while True:

	status,image = capture.read()
        if( status ):
            cv.imshow( "Camera", image )
            algoimage=doalgo( image)
            if( algoimage ):
                cv.imshow( "Algo", algoimage )
                del algoimage
            del image
	else:
		print "No Frame"

        if( cv.waitKey(10) != -1 ):
            break

