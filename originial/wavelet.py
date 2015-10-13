__author__ = 'hamdiahmadi'

import numpy
import pywt
import video
import file
import scipy

# num = [123,123,123],[456,21,31]
fileName = '../../13732_1062770107321_3577169_n.jpg'
fileName = '../../60.png'
Image = video.toGray(video.readImage(fileName))
# Image = [[1,0,0],[0,0,0],[0,0,0]]
print len(Image),len(Image[0])
# # print  Image[0][0]
# for x in range(0,30):
LL,(LH,HL,HH) = pywt.dwt2(Image, 'db1')

# print HL
# print len(HL[0])
# for x in HL:
#     print set(x)
# for x in range(0,len(LH)):
#     print LH[x]
video.saveFrame('HH1.png',abs(HH))
# print len(video.readImage("HH1.png")),len(video.readImage("HH1.png")[0])
video.saveFrame('LH1.png',abs(LH))
video.saveFrame('HL1.png',abs(HL))
video.saveFrame('LL1.png',abs(LL))

HH1 = video.readImage('HH1.png')
print len(HH1),len(HH1[0])
for x in range(500,len(HH1)):
    for y in range(0,len(HH1[x])):
        print HH1[x][y],HH[x][y]
    break