#!/bin/sh
F="~/vision_video/GENKI-R2009a.avi"
[ "x$1" != "x" ] && F=$1
for x in /home/gunnjo/NetSrc/opencv/data/haarcascades/haarcascade_frontalface_alt_tree.xml /home/gunnjo/NetSrc/opencv/data/haarcascades/haarcascade_frontalface_alt2.xml /home/gunnjo/NetSrc/opencv/data/haarcascades/haarcascade_frontalface_default.xml /home/gunnjo/NetSrc/opencv/data/haarcascades/haarcascade_frontalface_alt.xml
do
	for y in /home/gunnjo/NetSrc/opencv/data/haarcascades/haarcascade_eye.xml /home/gunnjo/NetSrc/opencv/data/haarcascades/haarcascade_eye_tree_eyeglasses.xml
	do
		RUN=`date "+%Y%m%d%H%M%S"`
		time python ./eyes.py  $F $x $y > $RUN.out 2>$RUN.err
	done
done
