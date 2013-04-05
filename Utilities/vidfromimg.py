import sys
import os
import re
import cv2
import cv2.cv as cv
import numpy as np

if __name__ == "__main__":
	re = re.compile("^.*\.(jpg|bmp)$")
	folder = "."
	video = "test.avi"
	writer = None
	h = 640
	w = 480
	vsize = (0,0)
	if len(sys.argv)==2 : folder = sys.argv[1]
	if len(sys.argv)==3 : video = sys.argv[2]

	for filename in os.listdir (folder):
		if (not re.match(filename)):
			continue
		img = cv2.imread(folder + filename)
		if ( img == None) :
			#ignore open error
			#print "failed to load", folder + filename
			continue
		if (writer == None):
			writer = cv2.VideoWriter(video, cv.CV_FOURCC('F','F','V','1'), 30, (w, h))
		img2 = np.zeros((h,w,3), np.uint8)
		if img.shape[0] <= h and img.shape[1] <= w :
			img2[0:img.shape[0], 0:img.shape[1]] = img
			writer.write(img2)
		else :
			print "Skipping", img.shape
