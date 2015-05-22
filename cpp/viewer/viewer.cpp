#include "opencv2/core.hpp"
#include <opencv2/core/utility.hpp>
#include "opencv2/imgproc.hpp"
#include "opencv2/calib3d.hpp"
#include "opencv2/imgcodecs.hpp"
#include "opencv2/videoio.hpp"
#include "opencv2/highgui.hpp"

#include <cctype>
#include <stdio.h>
#include <string.h>
#include <time.h>

#define MAX_PATH 100

using namespace cv;
using namespace std;

const char * usage =
" \nexample command line for viewing from a live feed.\n"
"   viewer \n"
" \n";




const char* liveCaptureHelp =
    "When the live video from camera is used as input, the following hot-keys may be used:\n"
        "  <ESC>, 'q' - quit the program\n"
        "  's' - capture image\n"
        "  '-' - zoom out\n"
        "  '+' - zoom in\n"
        "  'i' - zoom window in\n"
        "  'o' - zoom window out\n"
        "  'u' - shift window up\n"
        "  'd' - shift window down\n"
        "  'l' - shift left\n"        
        "  'r' - shift right\n";

static void help()
{
    printf( "This is a camera viewer sample.\n"
        "Usage: viewer\n"
        "\n" );
    printf("\n%s",usage);
    printf( "\n%s", liveCaptureHelp );
}

int main( int argc, char** argv )
{
    int i;
    int width = 1920, height = 1080;
    VideoCapture capture;
    int delay = 1000;
    int cameraId = 0;

    for( i = 1; i < argc; i++ )
    {
        const char* s = argv[i];
        if( strcmp( s, "-w" ) == 0 )
        {
            if( sscanf( argv[++i], "%u", &width ) != 1 || width <= 0 )
                return fprintf( stderr, "Invalid width\n" ), -1;
        }
        else if( strcmp( s, "-h" ) == 0 )
        {
            if( sscanf( argv[++i], "%u", &height ) != 1 || height <= 0 )
                return fprintf( stderr, "Invalid height\n" ), -1;
        }
        else if( strcmp( s, "-help" ) == 0 )
        {
            help();
            return 0;
        }
        else if( s[0] != '-' )
        {
            if( isdigit(s[0]) )
                sscanf(s, "%d", &cameraId);
            else
                fprintf( stderr, "Invalid Camera Id %s", s);
        }
        else
            return fprintf( stderr, "Unknown option %s", s ), -1;
    }

    capture.open(cameraId);

    if( !capture.isOpened() )
        return fprintf( stderr, "Could not initialize video (%d) capture\n",cameraId ), -2;

    capture.set(cv::CAP_PROP_FRAME_WIDTH, width);
    capture.set(cv::CAP_PROP_FRAME_HEIGHT, height);

    if( capture.isOpened() )
        printf( "%s", liveCaptureHelp );

    namedWindow( "Image View", cv::WINDOW_NORMAL );

    int wwidth = width, wheight = height;
    int vwidth = width, vheight = height;
    int top = 0, left = 0;
    resizeWindow("Image View", wwidth, wheight);

    for(;;)
    {
        int pindex = 0;
        Rect r(left, top, vwidth, vheight);
        Mat view0;
        capture >> view0;

        Mat view(view0, r);

        imshow("Image View", view);
        int key = 0xff & waitKey(50);

        if( (key & 255) == 27 )
            break;

        switch( key ) {
        case 's':
            {
                char m[MAX_PATH];
                sprintf(m, "image%04d.png", pindex);
                string s = imwrite( m, view) ? " Saved.": "fail to save" ;
                printf("%s: %s\n", m, s.c_str());
                pindex++;
            }
            break;
        case '+':
            vwidth = vwidth > 20 ?  vwidth-(vwidth/10) : 10;
            vheight = wheight > 20 ?  vheight-(vheight/10) : 10;
            break;
        case '-':
            vwidth = vwidth+(wwidth/10) >= width-left ?  width-left : vwidth+(wwidth/10);
            vheight = vheight+(wheight/10) >= height-top ?  height-top: vheight+(wheight/10);
            break;
        case 'u':
            top = top-(vheight/10) <= 0 ? 0: top-(vheight/10);
            break;
        case 'd':
            top = top+(vheight/10) >= height-vheight ? height-vheight : top+(vheight/10);
            break;
        case 'l':
            left = left < vwidth/10 ? 0 : left-(vwidth/10);
            break;
        case 'r':
            left = left+(vwidth/10) >= width-vwidth ? width-vwidth : left+vwidth/10;
            break;
        case 'i':
            wwidth = wwidth-(wwidth/10) > 20 ?  wwidth-(wwidth/10) : 10;
            wheight = wheight-(wheight/10) > 20 ? wheight-(wheight/10) : 10;
            resizeWindow("Image View", wwidth, wheight);
            break;
        case 'o':
            wwidth = wwidth+(wwidth/10) >= width ?  width : wwidth+(wwidth/10);
            wheight = wheight+(wheight/10) >= height ? height: wheight+(wheight/10);
            resizeWindow("Image View", wwidth, wheight);
            break;
        }
    }

    return 0;
}
