#!/usr/bin/python
import cv
import sys

def doalgo( image, model):
    cv.UpdateBGStatModel( image, model)
    return model.background

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
    if(cv.GrabFrame( capture ) ):
        image = cv.RetrieveFrame( capture )
    model = cv.CreateGaussianBGModel( image)
    while True:

        if(cv.GrabFrame( capture ) ):
            image = cv.RetrieveFrame( capture )
        if( image ):
            cv.ShowImage( "Camera", image )
            algoimage=doalgo( image, model)
            if( algoimage ):
                cv.ShowImage( "Algo", algoimage )
                del algoimage
            del image
        if( cv.WaitKey(10) != -1 ):
            break
    cv.DestroyWindow( "Camera" )
    cv.DestroyWindow( "Algo" )
