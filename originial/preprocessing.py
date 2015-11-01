__author__ = 'hamdiahmadi'
import numpy as np
import cv2

class c_data:

    def __init__(self):
        pass

    def getPower(self,data,n):
        return pow(data,n)

    def getExp(self,data,stdDev,mean):
        data = float(data)
        stdDev = float(stdDev)
        mean = float(mean)
        res = self.getPower((data-mean),2)
        div = 2*self.getPower(stdDev,2)
        return np.exp(-res/div)

    def getSquareRoot(self,data):
        return np.sqrt(data)

    def getGaussianProbability(self,data, stdDev, mean):
        exp = self.getExp(data,stdDev,mean)
        res = stdDev*self.getSquareRoot(2*np.pi)
        res = 1/res
        return res* exp

class pixelDetection(c_data):

    def __init__(self):
        c_data.__init__(self)
        self.threshold = pow(10,-9)

    def getGaussianProbability(self,data, stdDev, mean):
        blue = c_data.getGaussianProbability(self,data[0], stdDev[0], mean[0])
        green = c_data.getGaussianProbability(self,data[1], stdDev[1], mean[1])
        red = c_data.getGaussianProbability(self,data[2], stdDev[2], mean[2])
        return blue, green, red

    def probabilityDistribution(self,data, stdDev, mean):
        blue, green, red = self.getGaussianProbability(data,stdDev,mean)
        return blue*green*red

    def isCandidatePixel(self,data, stdDev, mean):
        if (self.probabilityDistribution(data, stdDev, mean)>self.threshold):
            return True
        return False

    def getCandidatePixel(self,list, image, stdDev, mean):
        truePixel = []
        falsePixel = []
        for x in range(0,len(list[0])):
            data = image[list[0][x]][list[1][x]]
            res = self.isCandidatePixel(data,stdDev,mean)
            if (res == True):
                truePixel.append([list[0][x],list[1][x]])
            else:
                falsePixel.append([list[0][x],list[1][x]])
        return truePixel,falsePixel