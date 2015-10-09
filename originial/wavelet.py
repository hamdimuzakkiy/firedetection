__author__ = 'hamdiahmadi'

import numpy
import pywt
import video

num = [123,123,123],[456,21,31]
fileName = '../../DSCF2007.JPG'
Image = video.toGray(video.readImage(fileName))
print Image[0][0]
# LL,(LH,HL,HH) = pywt.dwt(Image[0], 'db3')
# print HH