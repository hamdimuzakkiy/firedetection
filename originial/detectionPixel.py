__author__ = 'hamdiahmadi'
import os
import cv2
import data as dt

def getMean(list):
    sumValue = dt.sumArray(list)
    return sumValue/len(list)

def getStandardDeviation(list, mean):
    countData = len(list)
    list = list-mean
    list = list*list
    res = dt.sumArray(list)
    print res
    res = res / mean
    print res
    return dt.getSquareRoot(res)

def getPixelColorList(path):
    res = []
    listDir = os.listdir(path)
    for data in listDir :
        image = cv2.imread(path+'/'+data)
        pixel = dt.getDatasetPixel(image)
        res.extend(pixel)
    return res

def getStdDevAndMean(path):
    listColor = getPixelColorList(path)
    mean = getMean(listColor)
    standarDev = getStandardDeviation(listColor,mean)
    print standarDev
    # res = [[1,2,3],[2,3,4]]
    # res.append([1,2,3])
    return