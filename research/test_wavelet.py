__author__ = 'hamdiahmadi'
import pywt
import numpy
import cv2

image = cv2.imread('gambar2.JPG')
image = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
cv2.imwrite('gray.png',image)
# image = [[1,2,3,4],[1,2,3,4],[1,2,3,4],[1,2,3,4]]
app,(h,v,d) = pywt.dwt2(image,'db2')
cv2.imwrite('app.png',app)
cv2.imwrite('h.png',h)
cv2.imwrite('v.png',v)
cv2.imwrite('d.png',d)

