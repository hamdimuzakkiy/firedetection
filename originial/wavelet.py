import pywt

def toWavelet(image):
    return pywt.dwt2(image,'db2')