__author__ = 'hamdiahmadi'
import os
import cv2
import data as dt

def getMean(list):
    sumValue = dt.sumArray(list)
    sumValue = sumValue/len(list)
    sumValue = sumValue[0],sumValue[1],sumValue[2]
    return sumValue

def getStandardDeviation(list, mean):
    countData = len(list)
    list = dt.getPower(dt.getSubstractList(list,mean),2)
    list = dt.sumArray(list)/countData
    list = dt.getSquareRoot(list)
    res = [list[0],list[1],list[2]]
    return res

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
    return standarDev,mean

def getCandidatePixel(list, image, stdDev, mean):
    return