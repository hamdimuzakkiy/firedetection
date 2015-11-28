__author__ = 'hamdiahmadi'

import pywt
import numpy
import video
import cv2

baseHH = 'wv/HH'
baseLH = 'wv/LH'
baseHL = 'wv/HL'

coor_x = 94
coor_y = 52
list = []
for x in range (284,294):
    HH = cv2.imread(baseHH+'/'+str(x)+'.png')
    HL = cv2.imread(baseHL+'/'+str(x)+'.png')
    LH = cv2.imread(baseLH+'/'+str(x)+'.png')
    print HH[coor_y][coor_x],HL[coor_y][coor_x],LH[coor_y][coor_x]
