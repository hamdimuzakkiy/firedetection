__author__ = 'hamdiahmadi'
import numpy as np

#return pixel from moving - getMovingPixel
def getMovingPixel(file):
    listX,listY = np.where( file == 255 )
    return np.vstack((listX,listY))


