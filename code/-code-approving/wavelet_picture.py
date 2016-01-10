__author__ = 'hamdiahmadi'

import cv2
import pywt
import pylab

def toBNW(image):
    for y in range(0,len(image)):
        for x in range(0,len(image[y])):
            if image[y][x] > 0:
                image[y][x]*=4
    return image

image = cv2.imread('DSC02468.JPG')
image = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)

# for x in range(0,2):
#     image = cv2.pyrDown(image)

cv2.imwrite('gray.png',image)
a,(h,v,d) = pywt.dwt2(image,'db2')


cv2.imwrite('a.png',a)
cv2.imwrite('h.png',h)
cv2.imwrite('v.png',v)
cv2.imwrite('d.png',d)

list = []
list.append('a.png')
list.append('h.png')
list.append('v.png')
list.append('d.png')

for x in list:
    image = cv2.imread(x)
    image = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)

    if x != 'a.png':
        image = toBNW(image)
    cv2.imwrite(x,image)