__author__ = 'hamdiahmadi'
import numpy as np
import cv2

class c_data:

    def __init__(self):
        pass

    def getGaussianProbability(self,data, stdDev, mean):
        data = float(data)
        stdDev = float(stdDev)
        mean = float(mean)
        res = pow((data-mean),2)
        div = 2*pow(stdDev,2)
        exp = np.exp(-res/div)
        res = stdDev*np.sqrt(2*np.pi)
        res = 1/res
        return res* exp

    def getGaussianProbability2(self,valExp,allStdDev):
        exp = np.exp(valExp)
        #res = 1/(np.sqrt(2*np.pi))*allStdDev
        res = allStdDev
        return exp*res

class pixelDetection(c_data):

    def __init__(self):
        c_data.__init__(self)
        self.threshold = pow(10,-8)

    def getCandidatePixel(self,list, image, stdDev, mean):
        truePixel = []
        falsePixel = []

        for x in range(0,len(list[0])):
            data = image[list[0][x]][list[1][x]]
            valExp = (pow(float(data[0])-float(mean[0]),2)/(2*pow(stdDev[0],2)))+(pow(float(data[1])-float(mean[1]),2)/(2*pow(stdDev[1],2)))+(pow(float(data[2])-float(mean[2]),2)/(2*pow(stdDev[2],2)))
            valExp = -valExp
            allStdDev = 1/(float(stdDev[0])*float(stdDev[1])*float(stdDev[2]))
            res = c_data.getGaussianProbability2(self,valExp,allStdDev)
            if (res>self.threshold):
                truePixel.append([list[0][x],list[1][x]])
            else:
                falsePixel.append([list[0][x],list[1][x]])
        return truePixel,falsePixel


class intensityDetection(c_data):

    def __init__(self):
        c_data.__init__(self)

    def getCandidatePixel(self,image,listCandidate):
        truePixel = []
        falsePixel = []
        threshold = np.mean(image)
        for x in listCandidate:
            if image[x[0]][x[1]] > threshold:
                truePixel.append([x[0],x[1]])
            else:
                falsePixel.append([x[0],x[1]])
        return truePixel,falsePixel
