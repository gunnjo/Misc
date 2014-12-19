#!/usr/bin/env python

'''
K-means clusterization sample.
Usage:
   kmeans.py

Keyboard shortcuts:
   ESC   - exit
   space - generate new distribution
'''
import sys

import numpy as np
import cv2

def scaleshow( win, image):
    width = image.shape[1]
    height = image.shape[0]
    if ( width > 800 or height > 600 ):
       width = 800
       height = 600
    i = cv2.resize( image, (width, height), 0, 0, cv2.INTER_NEAREST)
    cv2.imshow( win, i )

if __name__ == '__main__':
    cluster_n = 2
    img_size = 512

    path = "x.tiff"

    if len(sys.argv)>1:
        path = sys.argv[1]

    if len(sys.argv)>2:
        cluster_n = int(sys.argv[2])
    print __doc__

    # generating bright palette

    image = cv2.imread( path)
    scaleshow('Orig', image)
    b,g,r  = cv2.split(image)
    rows, cols, layers =  image.shape
    points = (np.float32(g)+np.float32(r))/2.
    scaleshow('Gray', np.uint8(points))
#    points = np.float32(image)

    term_crit = (cv2.TERM_CRITERIA_EPS, 30, 0.1)
    ret, labels, centers = cv2.kmeans(points, cluster_n, None, term_crit, 10, 0)

    print labels
    print centers

    centers = np.uint8(centers)
    res = centers[labels.flatten()]
    img2 = res.reshape(points.shape)
    scaleshow('Result', img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
