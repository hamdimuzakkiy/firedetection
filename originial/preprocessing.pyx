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
        # res = stdDev*(2*np.pi)
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

    def getThreshold(self):
        return pow(10,-8)

    def getCandidatePixel(self,list, image, stdDev, mean):
        self.threshold = self.getThreshold()
        truePixel = []
        falsePixel = []
        for x in range(0,len(list[0])):
            data = image[list[0][x]][list[1][x]]
            if data[2] >= data[1] and data[1] >= data[0]:
                res = c_data.getGaussianProbability(self,data[0], stdDev[0], mean[0])* c_data.getGaussianProbability(self,data[1], stdDev[1], mean[1])* c_data.getGaussianProbability(self,data[2], stdDev[2], mean[2])
                if (res>self.threshold):
                    truePixel.append([list[0][x],list[1][x]])
                else:
                    falsePixel.append([list[0][x],list[1][x]])
            else :
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
        # gaussians = cv2.GaussianBlur((cv2.pyrUp(gaussians)),(5,5),0)
        return gaussians

    def getLuminanceImageGray(self,image):
        grayLuminance = imageProcessing.toGray(self,image)
        gaussianLuminance13 = copy.copy(grayLuminance)
        gaussianLuminance7 = copy.copy(grayLuminance)
        return self.toLuminance(gaussianLuminance7,gaussianLuminance13)

    def getLumiananceImage(self,image):
        grayLuminance = imageProcessing.toGray(self,image)

        gaussianLuminance13 = imageProcessing.gaussianFilter(self,copy.copy(grayLuminance),13)
        gaussianLuminance7 = imageProcessing.gaussianFilter(self,copy.copy(grayLuminance),7)

        return self.toLuminance(gaussianLuminance7,gaussianLuminance13)

class intensityDetection(c_data):

    def __init__(self):
        c_data.__init__(self)

    def getRangeFire(self,image,listCandidate,range,constanta):
        if len(listCandidate) == 0:
            return False,False,False,False

        listCandidates = np.array(listCandidate)

        minY,maxY =  min(listCandidates[:,0]),max(listCandidates[:,0])
        minX,maxX =  min(listCandidates[:,1]),max(listCandidates[:,1])

        constanta = 2
        constanta-=1
        par1 = maxX - minX
        par2 = maxY - minY

        maxRange = min(par1,par2)
        lenY = maxRange
        lenX = maxRange

        if minY - int(lenY*constanta) < 0:
            minY = 0
        else :
            minY = minY - int(lenY*constanta)

        if minX - int(lenX*constanta) < 0:
            minX = 0
        else :
            minX = minX - int(lenX*constanta)

        if int(maxY+lenY*constanta)>=len(image):
            maxY = int(len(image)-1)
        else:
            maxY = int(maxY+lenY*constanta)
        if int(maxX+lenX*constanta)>=len(image[0]):
            maxX = int(len(image)-1)
        else:
            maxX = int(maxX+lenX*constanta)

        return minY,minX,maxY,maxX

    def getRange(self,image,listCandidate,range,constanta):
        if len(listCandidate) == 0:
            return False,False,False,False

        minY,maxY =  min(range[0]),max(range[0])
        minX,maxX =  min(range[1]),max(range[1])

        constanta-=1
        par1 = maxX - minX
        par2 = maxY - minY

        maxRange = min(par1,par2)
        lenY = maxRange
        lenX = maxRange

        if minY - int(lenY*constanta) < 0:
            minY = 0
        else :
            minY = minY - int(lenY*constanta)

        if minX - int(lenX*constanta) < 0:
            minX = 0
        else :
            minX = minX - int(lenX*constanta)

        if int(maxY+lenY*constanta)>=len(image):
            maxY = int(len(image)-1)
        else:
            maxY = int(maxY+lenY*constanta)
        if int(maxX+lenX*constanta)>=len(image[0]):
            maxX = int(len(image[0])-1)
        else:
            maxX = int(maxX+lenX*constanta)

        return minY,minX,maxY,maxX

    #candidate pixel based on average intensity moving object with range 2* extrim point
    def getIntensityPixel(self,image,listCandidate,range):
        truePixel = []
        falsePixel = []
        if len(listCandidate) == 0:
            return truePixel,falsePixel

        constanta = 1.5
        minY,minX,maxY,maxX = self.getRange(copy.copy(image),copy.copy(listCandidate),copy.copy(range),constanta)

        if maxX == minX:
            maxX+=1
        if maxY == minY:
            maxY+=1

        image2 = copy.copy(image)
        image2 = image2[minY:maxY,minX:maxX]

        constanta = 1
        minY,minX,maxY,maxX = self.getRange(copy.copy(image),copy.copy(listCandidate),copy.copy(range),constanta)

        if maxX == minX:
            maxX+=1
        if maxY == minY:
            maxY+=1

        image3 = copy.copy(image)
        image3 = image3[minY:maxY,minX:maxX]

        sum2 = np.sum(image2)
        sum3 = np.sum(image3)

        threshold = (sum2-sum3)/((len(image2)*len(image2[0]))-(len(image3)*len(image3[0]))+1)

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

class growing(c_data,imageProcessing,colorDetection):

    def __init__(self):
        pass

    def doFloodFill(self, image,resImg ,is_visit, stack, regs, stdDev, mean, originalImage):
        res = []
        image = np.int_(image)
        self.threshold = colorDetection.getThreshold(self)
        clocks = c_data.clock(self)
        while len(stack) != 0:
            coory,coorx = stack[0]
            stack.pop(0)
            # resImg[coory][coorx] = 255
            res.append(image[coory][coorx])
            data = originalImage[coory][coorx]
            for x in clocks:
                if is_visit[coory+x[0]][coorx+x[1]] != 0 or coory+x[0] < 0 or coory+x[0] == len(image) or coorx+x[1] < 0 or coorx+x[1] == len(image[0]):
                    continue
                elif data[2] > data[1] and data[1] > data[0] and (int(image[coory][coorx])-int(image[coory+x[0]][coorx+x[1]])) < 50 and self.threshold < c_data.getGaussianProbability(self,data[0], stdDev[0], mean[0])* c_data.getGaussianProbability(self,data[1], stdDev[1], mean[1])* c_data.getGaussianProbability(self,data[2], stdDev[2], mean[2]):
                    is_visit[coory+x[0]][coorx+x[1]] = regs
                    stack.append([coory+x[0],coorx+x[1]])
        return resImg,is_visit,res

    def getRegion(self,list,images,stdDev, mean,counter):
        truePixel = []
        falsePixel = []
        grayImage = imageProcessing.toGray(self,images)
        is_visit = grayImage*0
        resImg = copy.copy(grayImage)
        regs = 0
        is_fire = dict()
        for x in list:
            coor_y = x[0]
            coor_x = x[1]
            if is_visit[coor_y][coor_x] == 0:
                stack = []
                regs+=1
                stack.append([coor_y,coor_x])
                resImg, is_visit, res = self.doFloodFill(grayImage,resImg,is_visit,stack,regs,stdDev, mean, images)
                if np.std(res) > 20:
                    is_fire[regs] = True
                    truePixel.append([coor_y,coor_x])
                else :
                    is_fire[regs] = False
                    falsePixel.append([coor_y,coor_x])
            else:
                if is_fire[is_visit[coor_y][coor_x]] == True:
                    truePixel.append([coor_y,coor_x])
                else :
                    falsePixel.append([coor_y,coor_x])
        return truePixel,falsePixel