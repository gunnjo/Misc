#!/usr/bin/python
import cv
import sys

def doalgo( image):
        newimage = cv.CreateMat(image.height*2, image.width*2, cv.CV_8UC3)
        cv.Resize( image, newimage)
        cascade = cv.Load("/usr/share/opencv/haarcascades//haarcascade_frontalface_alt.xml")
        mem = cv.CreateMemStorage(0);
        if( cascade ):
                faces = cv.HaarDetectObjects(newimage, cascade, mem, 1.2, 2, cv.CV_HAAR_DO_CANNY_PRUNING, (image.height/3, image.width/3))
                if( len(faces) ):
                        for (x,y,w,h),n in faces:
                            cv.Rectangle(newimage, (x,y), (x+w,y+h), 255)
        del mem;
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
