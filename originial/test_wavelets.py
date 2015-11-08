__author__ = 'hamdiahmadi'

import pywt
import numpy
import video
import cv2

img = video.toGray(video.readImage("wv/0.png"))
img = cv2.pyrUp(cv2.pyrUp(img))
cA, (cH, cV, cD) = pywt.dwt2(img,'db1')

print cA[66][79]
print cH[66][79]
print cV[66][79]
print cD[66][79]


video.saveFrame("wv/cA443_.png",cA)
video.saveFrame("wv/cH443_.png",cH)
video.saveFrame("wv/cV443_.png",cV)
video.saveFrame("wv/cD443_.png",cD)

cA = video.readImage("wv/cA443_.png")
cH = video.readImage("wv/cH443_.png")
cV = video.readImage("wv/cV443_.png")
cD = video.readImage("wv/cD443_.png")


print "----"

print cA[66][79]
print cH[66][79]
print cV[66][79]
print cD[66][79]