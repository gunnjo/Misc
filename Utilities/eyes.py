import sys
import cv
import cv2
import numpy as np

imageCount = 0
faceCount = 0
eyeCount = 0
#faceFile = "/home/gunnjo/NetSrc/opencv/data/haarcascades/haarcascade_frontalface_alt.xml"
faceFile = "/home/gunnjo/NetSrc/opencv/data/haarcascades/haarcascade_frontalface_default.xml"
eyeFile = "/home/gunnjo/NetSrc/opencv/data/haarcascades/haarcascade_eye.xml"
eyeFile = "/home/gunnjo/NetSrc/opencv/data/haarcascades/haarcascade_eye_tree_eyeglasses.xml"

def Load():
	faceCascade = cv2.CascadeClassifier(faceFile)
	eyeCascade = cv2.CascadeClassifier(eyeFile)
	return (faceCascade, eyeCascade)

def DetectEyes(image, faceCascade, eyeCascade):
	global faceCount, eyeCount
	min_size = (30,30)
	eye_size = (20,20)
	haar_scale = 1.1
	min_neighbors = 2
	haar_flags = 0
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# Equalize the histogram
	cv2.equalizeHist(gray)
	# Detect the faces
	faces = faceCascade.detectMultiScale(gray, haar_scale,
		min_neighbors, haar_flags, min_size)
	# If faces are found
	faceFound = 0
	for (x, y, w, h) in faces:
		faceFound+=1
		pt1 = (x , y )
		pt2 = ((x + w), (y + h))
		cv2.rectangle(image, pt1, pt2, cv.RGB(255, 0, 0), 3, 8, 0)
		# Estimate the eyes position
		# First, set the image region of interest
		# The last division removes the lower part of the face to lower probability for false recognition


		# Detect the eyes
		smallImage = image[y:y+(h*.7), x:(x+w)]
		print "x:", x, "y:", y, "dx:", w, "dy", h
		eyes = eyeCascade.detectMultiScale( smallImage,
			haar_scale, min_neighbors,
			haar_flags, eye_size)

		# If eyes were found
		print "Eyes ",len(eyes)
		# For each eye found
		eyeFound = 0
		for (ex, ey,ew,eh) in eyes:
			eyeFound+=1
			# Draw a rectangle around the eye
			cv2.rectangle(image,
				(ex+pt1[0],
				ey+pt1[1]),
				(ex+pt1[0]+ew,
				ey++pt1[1]+eh),
				cv.RGB(255, 0, 0), 1, 8, 0)

		if ( eyeFound > 0):
			eyeCount+=1
	if ( faceFound > 0):
		faceCount+=1
	return image

def GoAway():
	print "Images", imageCount, "faces", faceCount, "eyes", eyeCount, "faceCascade", faceFile, "eyeCascade", eyeFile
	exit()

if __name__ == "__main__":
	if len(sys.argv)==1:
		capture = cv2.VideoCapture( 0 )
	elif len(sys.argv)>1 and sys.argv[1].isdigit():
		capture = cv2.VideoCapture( int(sys.argv[1]) )
	elif len(sys.argv)>1:
		capture = cv2.VideoCapture( sys.argv[1] )

	if (len(sys.argv) > 2):
		faceFile = sys.argv[2]

	if len(sys.argv)>3:
		eyeFile = sys.argv[3]

	cv2.namedWindow("w1")
	faceCascade, eyeCascade = Load()
	endit = 1
	while endit:
		(ret, image) = capture.read()
		if ( ret):
			imageCount+=1
			image = DetectEyes(image, faceCascade, eyeCascade)
			cv2.imshow("w1", image)
#			if (cv2.waitKey(10000) == 27):
#				endit = 0
		else : endit = 0
	GoAway()
