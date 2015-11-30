__author__ = 'hamdiahmadi'
import numpy as np
import sys
import cv2
import excel
import copy

np.set_printoptions(threshold=sys.maxint)

class imageProcessing:
    def __init__(self):
        pass
    def toGray(self,image):
        return cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    def gaussianFilter(self,image,filters):
        return cv2.blur(image,(filters,filters))

class c_data:

    def __init__(self):
        pass

    def clock(self):
        clocks = []
        clocks.append([-1,-1])
        clocks.append([-1,0])
        clocks.append([-1,1])
        clocks.append([0,-1])
        clocks.append([0,1])
        clocks.append([1,-1])
        clocks.append([1,0])
        clocks.append([1,1])
        return clocks

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

    def getLuminanceDeviation(self,data):
        sumA = 0
        sumB = 0
        for x in range(0,len(data)):
            sumA+=((x+1)*data[x])
            sumB+=data[x]
        mean = float(sumA)/float(sumB)
        sumA=0
        for x in range(0,len(data)):
            sumA+=(pow(x+1-mean,2)*data[x])
        return float(sumA)/float(sumB)

    def getNormalRange(self,data):
        max = float(np.max(data))
        min = float(np.min(data))

        res = []
        for x in data:
            try :
                tmp = (float(x)-min)/(max-min)
            except:
                tmp = 0
            float('%.2f' % round(tmp))
            res.append(tmp)
        return res

class colorDetection(c_data):

    def __init__(self):
        c_data.__init__(self)

    def getCandidatePixel(self,list, image, stdDev, mean):
        self.threshold = 5*pow(10,-9)
        truePixel = []
        falsePixel = []
        for x in range(0,len(list[0])):
            data = image[list[0][x]][list[1][x]]
            res = c_data.getGaussianProbability(self,data[0], stdDev[0], mean[0])* c_data.getGaussianProbability(self,data[1], stdDev[1], mean[1])* c_data.getGaussianProbability(self,data[2], stdDev[2], mean[2])
            if (res>self.threshold):
                truePixel.append([list[0][x],list[1][x]])
            else:
                falsePixel.append([list[0][x],list[1][x]])
        return truePixel,falsePixel

class luminance(c_data,imageProcessing):

    def __init__(self):
        c_data.__init__(self)

    def toLuminance(self,gaussianLuminance7,gaussianLuminance13):
        # get max and min image , normalization image
        max7,max13 = np.max(gaussianLuminance7),np.max(gaussianLuminance13)
        min7,min13 = np.min(gaussianLuminance7),np.min(gaussianLuminance13)
        if (max7-min7 == 0):
            max7+=1
        if (max13-min13 == 0):
            max13+=1
        gaussianLuminance7-=min7
        gaussianLuminance13-=min13
        gaussianLuminance7*=(255/(max7-min7))
        gaussianLuminance13*=(255/(max13-min13))
        gaussians = cv2.add((gaussianLuminance7),(gaussianLuminance13))
        # gaussians = cv2.GaussianBlur((gaussians),(5,5),0)
        return gaussians

    def getLuminanceImageGray(self,image):
        grayLuminance = imageProcessing.toGray(self,image)
        gaussianLuminance13 = grayLuminance
        gaussianLuminance7 = grayLuminance
        return self.toLuminance(gaussianLuminance7,gaussianLuminance13)

    def getLumiananceImage(self,image):
        grayLuminance = imageProcessing.toGray(self,image)
        gaussianLuminance13 = imageProcessing.gaussianFilter(self,grayLuminance,13)
        gaussianLuminance7 = imageProcessing.gaussianFilter(self,grayLuminance,7)
        return self.toLuminance(gaussianLuminance7,gaussianLuminance13)

class intensityDetection(c_data):

    def __init__(self):
        c_data.__init__(self)

    #candidate pixel based on average intensity moving object with range 2* extrim point
    def getIntensityPixel(self,image,listCandidate,range):
        truePixel = []
        falsePixel = []
        if len(listCandidate) == 0:
            return truePixel,falsePixel

        minY,maxY =  min(range[0]),max(range[0])
        minX,maxX =  min(range[1]),max(range[1])
        const = 2

        if minY - (minY/const) < 0:
            minY = 0
        else :
            minY = minY - (minY/const)

        if minX - (minX/const) < 0:
            minX = 0
        else :
            minX = minX - (minX/const)

        if maxY*const>len(image):
            maxY = len(image)-1
        else:
            maxY = maxY*const
        if maxX*const>len(image):
            maxX = len(image)-1
        else:
            maxX = maxX*const
        image2 = copy.copy(image)
        image2 = image2[minY:maxY,minX:maxX]
        threshold = np.average(image2)
        for x in listCandidate:
            if image[x[0]][x[1]] > threshold:
                truePixel.append([x[0],x[1]])
            else:
                falsePixel.append([x[0],x[1]])
        return truePixel,falsePixel

    #candidate pixel based on x,y pixel with 10 frame
    def getDiferencePixel(self,listImage,listCandidate):
        truePixel = []
        falsePixel = []
        for x in listCandidate:
            arr = []
            for y in listImage:
                arr.append(y[x[0]][x[1]])
            res = float(np.std(arr))

            if (res > 5 and res < 30):
                truePixel.append([x[0],x[1]])
            else:
                falsePixel.append([x[0],x[1]])

        return truePixel,falsePixel