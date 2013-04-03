import sys
import cv
import cv2
import numpy as np

def Load():
	faceCascade = cv2.CascadeClassifier("/usr/share/haarcascade.xml")
	eyeCascade = cv2.CascadeClassifier("/usr/share/haarcascade_eye.xml")
	return (faceCascade, eyeCascade)

def DetectRedEyes(image, faceCascade, eyeCascade):

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
	for (x, y, w, h) in faces:
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
		for (ex, ey,ew,eh) in eyes:
			# Draw a rectangle around the eye
			cv2.rectangle(image,
				(ex+pt1[0],
				ey+pt1[1]),
				(ex+pt1[0]+ew,
				ey++pt1[1]+eh),
				cv.RGB(255, 0, 0), 1, 8, 0)

	return image

if __name__ == "__main__":
	if len(sys.argv)==1:
		capture = cv2.VideoCapture( 0 )
	elif len(sys.argv)==2 and sys.argv[1].isdigit():
		capture = cv2.VideoCapture( int(sys.argv[1]) )
	elif len(sys.argv)==2:
		capture = cv2.VideoCapture( sys.argv[1] )

	cv2.namedWindow("w1")
	faceCascade, eyeCascade = Load()
	endit = 1
	while endit:
		(ret, image) = capture.read()
		image = DetectRedEyes(image, faceCascade, eyeCascade)
		cv2.imshow("w1", image)
		if (cv2.waitKey(10000) == 27):
			endit = 0
