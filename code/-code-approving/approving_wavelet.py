__author__ = 'hamdiahmadi'


import cv2
import numpy as np
import pywt


def coeficient():
    h = []
    h.append((1+np.sqrt(3))/(4*np.sqrt(2)))
    h.append((3+np.sqrt(3))/(4*np.sqrt(2)))
    h.append((3-np.sqrt(3))/(4*np.sqrt(2)))
    h.append((1-np.sqrt(3))/(4*np.sqrt(2)))
    g = []
    g.append((1-np.sqrt(3))/(4*np.sqrt(2)))
    g.append((-3+np.sqrt(3))/(4*np.sqrt(2)))
    g.append((3+np.sqrt(3))/(4*np.sqrt(2)))
    g.append((-1-np.sqrt(3))/(4*np.sqrt(2)))
    return h,g

def rowWavelet(image):
    h,g = coeficient()
    if len(image[0])%2 == 1:
        new_col = len(image[0])/2+2
    else:
        new_col = len(image[0])/2+1
    res_low = np.ndarray(shape=(len(image),new_col))
    res_high = np.ndarray(shape=(len(image),new_col))
    for row in range(0,len(image)):
        start = -2
        for col in range(0,new_col):
            tmp_high = 0
            tmp_low = 0
            for x in range(0,len(h)):
                if start+x<0:
                    tmp_low+=(h[x]*image[row][-(start+x)-1])
                    tmp_high+=(g[x]*image[row][-(start+x)-1])
                elif start+x>=len(image[0]):
                    tmp_low+=(h[x]*image[row][2*(len(image[0]))-(start+x)-1])
                    tmp_high+=(g[x]*image[row][2*(len(image[0]))-(start+x)-1])
                else :
                    tmp_low+=(h[x]*image[row][start+x])
                    tmp_high+=(g[x]*image[row][start+x])
            start+=2
            res_low[row][col] = tmp_low
            res_high[row][col] = tmp_high
    return res_low,res_high

def colWavelet(image):
    h,g = coeficient()
    if len(image[0])%2 == 1:
        new_row = len(image)/2+2
    else:
        new_row = len(image)/2+1
    res_low = np.ndarray(shape=(new_row,len(image[0])))
    res_high = np.ndarray(shape=(new_row,len(image[0])))
    for col in range(0,len(image[0])):
        start = -2
        for row in range(0,new_row):
            tmp_high = 0
            tmp_low = 0
            for x in range(0,len(h)):
                if start+x<0:
                    tmp_low+=(h[x]*image[-(start+x)-1][col])
                    tmp_high+=(g[x]*image[-(start+x)-1][col])
                elif start+x>=len(image):
                    tmp_low+=(h[x]*image[2*(len(image))-(start+x)-1][col])
                    tmp_high+=(g[x]*image[2*(len(image))-(start+x)-1][col])
                else :
                    tmp_low+=(h[x]*image[start+x][col])
                    tmp_high+=(g[x]*image[start+x][col])
            start+=2
            res_low[row][col] = tmp_low
            res_high[row][col] = tmp_high
    return res_low,res_high

def wavelet(image):
    row_low,row_high = rowWavelet(image)
    approx,horizontal = colWavelet(row_low)
    vertikal,diagonal = colWavelet(row_high)
    return approx,horizontal,vertikal,diagonal

if __name__ == '__main__':
    image = cv2.imread('DSCF2037.JPG')
    for x in range(0,3):
        image = cv2.pyrDown(image)
    image = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    a,h,v,d = wavelet(image)
    # a,(h,v,d) = pywt.dwt2(image,'db2')
    cv2.imwrite('a.png',a)
    cv2.imwrite('h.png',h)
    cv2.imwrite('v.png',v)
    cv2.imwrite('d.png',d)