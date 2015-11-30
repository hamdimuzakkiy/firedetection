__author__ = 'hamdiahmadi'
import pywt
import numpy as np

def toWavelet(image):
    return pywt.dwt2(image,'db4')

def getWaveletValue(coory,coorx,wavelet):
    # coory = coory/2
    # coorx = coorx/2
    res = []

    for x in wavelet:
        # if (x[0][coory][coorx]<0):
        #     x[0][coory][coorx] = 0
        # if (x[1][coory][coorx]<0):
        #     x[1][coory][coorx] = 0
        # if (x[2][coory][coorx]<0):
        #     x[2][coory][coorx] = 0
        # print x[0][coory][coorx],x[1][coory][coorx],x[2][coory][coorx]
        result = np.power(x[0][coory][coorx],2)+np.power(x[1][coory][coorx],2)+np.power(x[2][coory][coorx],2)
        result = float('%.1f' % round(result, 2))
        res.extend([result])
    return res

def setData():
    res = []
    for x in range(0,10):
        res.append([0,0,0])
    return res
