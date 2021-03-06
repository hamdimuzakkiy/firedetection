__author__ = 'hamdiahmadi'
import numpy as np
import copy

#return pixel from moving - getMovingPixel
def getMovingPixel(data):
    listY,listX = np.where( data == 255 )
    return np.vstack((listY,listX))

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
#get sqrt data
def getSquareRoot(data):
    return np.sqrt(data)
#get substract list of tuple with tuple
def getSubstractList(data,substractor):
    for x in range(0,len(data)):
        data[x] = int(data[x][0])-int(substractor[0]),int(data[x][1])-int(substractor[1]),int(data[x][2])-int(substractor[2])
    return data

def getPower(data,n):
    return np.power(data,n)

def getExp(data, stdDev,mean):
    data = float(data)
    stdDev = float(stdDev)
    mean = float(mean)
    res = getPower((data-mean),2)
    div = 2*getPower(stdDev,2)
    return np.exp(-res/div)

def getGaussianProbability(data, stdDev, mean):
    exp = getExp(data,stdDev,mean)
    res = stdDev*getSquareRoot(2*np.pi)
    res = 1/res
    return res* exp

def getNormalRange(data):
    max = np.max(data)
    mins = np.min(data)
    if max == 0:
        max = 1
    res = []
    for x in data:
        try:
            tmp = (float(x)-float(mins))/(float(max)-float(mins)+1)
        except:
            tmp = 0
        tmp = float('%.2f' % tmp)
        res.append(tmp)

    res = np.sort(res)
    return res

def getNormalRange2(data,image):
    max0 = pow(np.max(image[0]),2)
    max1 = pow(np.max(image[1]),2)
    max2 = pow(np.max(image[2]),2)
    min0 = pow(np.min(image[0]),2)
    min1 = pow(np.min(image[1]),2)
    min2 = pow(np.min(image[2]),2)
    max = max0+max1+max2
    mins = min0+min1+min2
    if max == 0:
        max = 1
    res = []
    for x in data:
        try:
            tmp = (float(x)-float(mins))/(float(max)-float(mins))
        except:
            tmp = 0
        tmp = float('%.2f' % tmp)
        res.append(tmp)
    res = np.sort(res)
    return res

def getStdev(arr):
    return np.std(arr)

def getAverage(arr):
    return np.average(arr)

def getSort(arr):
    return np.sort(arr)

def sum2D(data):
    return sum(map(sum, data))
