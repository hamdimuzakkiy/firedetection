__author__ = 'hamdiahmadi'
import numpy as np
import cv2

#return pixel from moving - getMovingPixel
def getMovingPixel(data):
    listX,listY = np.where( data == 255 )
    return np.vstack((listX,listY))

def toBooleanImage(data):
    return data/255

#convert to 3d
def to3Dimension(data):
    return np.dstack((data,data,data))

#get colored pixel in dataset ( no 0,0,0 )
def getDatasetPixel(data):
    arr = []
    res = np.where(data != [0,0,0])
    for x in range(0,len(res[0]),3) :
        arrays = data[res[0][x]][res[1][x]][0],data[res[0][x]][res[1][x]][1],data[res[0][x]][res[1][x]][2]
        arr.append(arrays)
    return arr

#sum array for sum data set R,G,B
def sumArray(data):
    return np.sum(data,axis=0)

def getSquareRoot(data):
    return np.sqrt(data)