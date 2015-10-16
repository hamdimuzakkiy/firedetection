__author__ = 'hamdiahmadi'
import pywt
import numpy as np

def toWavelet(image):
    return pywt.dwt2(image,'db4')

def getWaveletValue(coory,coorx,wavelet):
    coory = coory/2
    coorx = coorx/2
    res = []
    for x in wavelet:
        res.extend([np.power(x[0][coory][coorx],2)+np.power(x[1][coory][coorx],2)+np.power(x[2][coory][coorx],2)])
    return res

def setData():
    res = []
    for x in range(0,10):
        res.append([0,0,0])
    return res