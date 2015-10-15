__author__ = 'hamdiahmadi'
import pywt
import video

def toWavelet(image):
    return pywt.dwt2(image,'db4')