#!/bin/sh
for x in /home/gunnjo/NetSrc/opencv/data/haarcascades/haarcascade_frontalface_alt_tree.xml /home/gunnjo/NetSrc/opencv/data/haarcascades/haarcascade_frontalface_alt2.xml /home/gunnjo/NetSrc/opencv/data/haarcascades/haarcascade_frontalface_default.xml /home/gunnjo/NetSrc/opencv/data/haarcascades/haarcascade_frontalface_alt.xml
do
	for y in /home/gunnjo/NetSrc/opencv/data/haarcascades/haarcascade_eye.xml /home/gunnjo/NetSrc/opencv/data/haarcascades/haarcascade_eye_tree_eyeglasses.xml
	do
		RUN=`date "+%Y%m%d%H%M"`
		time python ./eyes.py  ~/vision_video/GENKI-R2009a.avi $x $y > $RUN.out 2>$RUN.err
	done
done
