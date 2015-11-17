__author__ = 'hamdiahmadi'

import pywt
import numpy
import video
import cv2

img = video.toGray(video.readImage("wv/FIREGENB.jpg"))
print(img)
cA, (cH, cV, cD) = pywt.dwt2(img,'db1')

video.saveFrame("wv/cA443_.png",cA)
video.saveFrame("wv/cH443_.png",cH)
video.saveFrame("wv/cV443_.png",cV)
video.saveFrame("wv/cD443_.png",cD)
