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
        res.append((float(x)-float(mins))/(float(max)-float(mins)))
    res = np.sort(res)
    res2 = copy.copy(res)
    for x in range(0,len(res)-1):
        res[x] = res[x+1]-res[x]
    res = np.sort(res)

    return res,res2

def getStdev(arr):
    return np.std(arr)

def getAverage(arr):
    return np.average(arr)

def getSort(arr):
    return np.sort(arr)

def sum2D(data):
    return  sum(map(sum, data))
