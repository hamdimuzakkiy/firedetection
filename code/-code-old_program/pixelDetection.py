__author__ = 'hamdiahmadi'
import excel
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

def getGaussianProbability(data, stdDev, mean):
    blue = dt.getGaussianProbability(data[0], stdDev[0], mean[0])
    green = dt.getGaussianProbability(data[1], stdDev[1], mean[1])
    red = dt.getGaussianProbability(data[2], stdDev[2], mean[2])
    return blue, green, red

def probabilityDistribution(data, stdDev, mean):
    blue, green, red = getGaussianProbability(data,stdDev,mean)
    return blue*green*red

def isCandidatePixel(data, stdDev, mean):
    global threshold
    if (probabilityDistribution(data, stdDev, mean)>threshold):
        return True
    return False

def getCandidatePixel(list, image, stdDev, mean):
    truePixel = []
    falsePixel = []

    for x in range(0,len(list[0])):
        data = image[list[0][x]][list[1][x]]
        if (isCandidatePixel(data,stdDev,mean) == True):
            truePixel.append([list[0][x],list[1][x]])
        else:
            falsePixel.append([list[0][x],list[1][x]])
    return truePixel,falsePixel

threshold = pow(10,-8)

