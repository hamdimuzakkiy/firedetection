__author__ = 'hamdiahmadi'
import numpy as np
import sys
import cv2
import excel
import copy
import os

np.set_printoptions(threshold=sys.maxint)

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

    def getDatasetPixel(data):
        arr = []
        res = np.where(data != [0,0,0])
        for x in range(0,len(res[0]),3) :
            arrays = data[res[0][x]][res[1][x]][0],data[res[0][x]][res[1][x]][1],data[res[0][x]][res[1][x]][2]
            arr.append(arrays)
        return arr

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

    def getMaxList(self,data):
        return np.max(data)

    def getMinList(self,data):
        return np.min(data)

class imageProcessing:
    def __init__(self):
        pass
    def toGray(self,image):
        return cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    def gaussianFilter(self,image,filters):
        return cv2.blur(image,(filters,filters))
    def downSize(self,image):
        return cv2.pyrDown(image)
    def upSize(self,image):
        return cv2.pyrUp(image)

class colorDetection(c_data,file):

    def __init__(self):
        c_data.__init__(self)

    def getThreshold(self):
        return 5*pow(10,-9)

    def retriveColorList(self):
        lists = [[[False for k in xrange(256)] for j in xrange(256)]for i in xrange(256)]
        data = open('color.txt','r')
        for x in data:
            color = (x.split('\n')[0]).split(' ')
            lists[int(color[0])][int(color[1])][int(color[2])] = True
        return lists

    def getListColorPixel(self,stdDev,mean):
        res = []
        threshold = self.getThreshold()
        for B in range(0,256):
            for G in range(B,256):
                for R in xrange(G,256):
                    if c_data.getGaussianProbability(self,B, stdDev[0], mean[0])* c_data.getGaussianProbability(self,G, stdDev[1], mean[1])* c_data.getGaussianProbability(self,R, stdDev[2], mean[2]) > threshold:
                        # lists[B][G][R] = True
                        res.append([B,G,R])
        return res

    def getColorCandidatePixel2(self,list, image, dataset):
        truePixel = []
        falsePixel = []
        for x in range(0,len(list[0])):
            data = image[list[0][x]][list[1][x]]
            B,G,R = data[0],data[1],data[2]
            if dataset[B][G][R] == True:
                truePixel.append([list[0][x],list[1][x]])
            else :
                falsePixel.append([list[0][x],list[1][x]])
        return truePixel,falsePixel

    def getColorCandidatePixel(self,list, image, stdDev, mean):
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
        max7,max13 = c_data.getMaxList(self,gaussianLuminance7),c_data.getMaxList(self,gaussianLuminance13)
        min7,min13 = c_data.getMinList(self,gaussianLuminance7),c_data.getMinList(self,gaussianLuminance13)

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
        # grayLuminance = imageProcessing.downSize(self,grayLuminance)
        gaussianLuminance13 = imageProcessing.gaussianFilter(self,copy.copy(grayLuminance),13)
        gaussianLuminance7 = imageProcessing.gaussianFilter(self,copy.copy(grayLuminance),7)
        # res = imageProcessing.upSize(self,self.toLuminance(gaussianLuminance7,gaussianLuminance13))
        res = self.toLuminance(gaussianLuminance7,gaussianLuminance13)
        # res = cv2.GaussianBlur(res,(5,5),0)
        return res

class intensityDetection(c_data):

    def __init__(self):
        c_data.__init__(self)

    def getRangeConstant(self,images,listCandidate,constanta):
        minY,minX = c_data.getMinList(self,listCandidate[0]),c_data.getMinList(self,listCandidate[1])
        maxY,maxX = c_data.getMaxList(self,listCandidate[0]),c_data.getMaxList(self,listCandidate[1])

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

        if int(maxY+lenY*constanta)>=len(images):
            maxY = int(len(images)-1)
        else:
            maxY = int(maxY+lenY*constanta)
        if int(maxX+lenX*constanta)>=len(images[0]):
            maxX = int(len(images[0])-1)
        else:
            maxX = int(maxX+lenX*constanta)

        return minY,minX,maxY,maxX

    def getLuminanceCandidatePixel(self, image, listCandidate, region):
        truePixel = []
        falsePixel = []
        threshold = dict()
        listRegion = np.unique(region)
        for x in range(1,len(listRegion)):
            lists = np.where(region == x)
            minY,minX = c_data.getMinList(self,lists[0]),c_data.getMinList(self,lists[1])
            maxY,maxX = c_data.getMaxList(self,lists[0]),c_data.getMaxList(self,lists[1])
            candidateObject = copy.copy(image)[minY:maxY,minX:maxX]
            minY,minX,maxY,maxX = self.getRangeConstant(image,lists,1.5)
            aroundObject = copy.copy(image)[minY:maxY,minX:maxX]
            sumCandaidate = np.sum(candidateObject)
            sumArround = np.sum(aroundObject)
            try:
                threshold[x] = (sumArround-sumCandaidate)/((len(aroundObject)*len(aroundObject[0]))-(len(candidateObject)*len(candidateObject[0]))+1)
            except:
                threshold[x] = 255
        for x in listCandidate:
            coor_y = x[0]
            coor_x = x[1]
            if image[coor_y][coor_x] >= threshold[region[coor_y][coor_x]]:
                truePixel.append([coor_y,coor_x])
            else:
                falsePixel.append([coor_y,coor_x])
        return truePixel,falsePixel

    def getDiferencePixel(self,listImage,listCandidate):
        truePixel = []
        falsePixel = []
        for x in listCandidate:
            arr = []
            for y in listImage:
                arr.append(y[x[0]][x[1]])
            res = float(np.std(arr))
            if (res > 2 and res < 40):
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
            resImg[coory][coorx] = 255
            res.append(image[coory][coorx])
            data = originalImage[coory][coorx]
            for x in clocks:
                if  coory+x[0] < 0 or coory+x[0] == len(image) or coorx+x[1] < 0 or coorx+x[1] == len(image[0]) or is_visit[coory+x[0]][coorx+x[1]] != 0:
                    continue
                elif data[2] > data[1] and data[1] > data[0] and (int(image[coory][coorx])-int(image[coory+x[0]][coorx+x[1]])) < 50 and self.threshold < c_data.getGaussianProbability(self,data[0], stdDev[0], mean[0])* c_data.getGaussianProbability(self,data[1], stdDev[1], mean[1])* c_data.getGaussianProbability(self,data[2], stdDev[2], mean[2]):
                    is_visit[coory+x[0]][coorx+x[1]] = regs
                    stack.append([coory+x[0],coorx+x[1]])
        return resImg,is_visit,res

    def getGrowingRegion(self,list,images,stdDev,mean):
        grayImage = imageProcessing.toGray(self,images)
        is_visit = grayImage*0
        resImg = copy.copy(grayImage)
        region = 0
        for x in list:
            coor_y = x[0]
            coor_x = x[1]
            if is_visit[coor_y][coor_x] == 0:
                stack = []
                region+=1
                stack.append([coor_y,coor_x])
                is_visit[coor_y][coor_x] = region
                resImg, is_visit, res = self.doFloodFill(grayImage,resImg,is_visit,stack,region,stdDev, mean, images)
        return is_visit

    def getVarianceColorRegion(self,image,listCandidate,region):
        truePixel = []
        falsePixel = []
        listRegion = np.unique(region)
        image = imageProcessing.toGray(self,image)
        threshold = dict()
        for x in range(1,len(listRegion)):
            lists = np.where(region == x)
            res = []
            for y in range(0,len(lists[0])):
                res.append(image[lists[0][y]][lists[1][y]])
            std = np.std(res)
            if std > 20 and len(res) > 25:
                threshold[x] = True
            else :
                threshold[x] = False
        for x in listCandidate:
            coor_y = x[0]
            coor_x = x[1]
            if threshold[region[coor_y][coor_x]] == True:
                truePixel.append([coor_y,coor_x])
            else :
                falsePixel.append([coor_y,coor_x])
        return truePixel,falsePixel

    def getGrowingVarianceWide(self,listGrowing,listCandidate):
        truePixel = []
        falsePixel = []
        for x in listCandidate:
            lists = []
            coor_y = x[0]
            coor_x = x[1]
            for y in listGrowing:
                val = y[coor_y][coor_x]
                if val == 0:
                    continue
                lists.append(float(len(np.where(y == val)[0])))
            res_np = np.std(lists)
            # print res_np
            if res_np >= np.min(lists)/5:
                truePixel.append([coor_y,coor_x])
            else :
                falsePixel.append([coor_y,coor_x])
        return truePixel,falsePixel

    def getGrowingCenterPoint(self,listGrowing,listCandidate):
        truePixel = []
        falsePixel = []
        ref = []
        for x in listGrowing:
            res = dict()
            listRegion = np.unique(x)
            for val in listRegion :
                if val == 0:
                    continue
                reg = (np.where(x == val))
                minY,minX,maxY,maxX = np.min(reg[0]),np.min(reg[1]),np.max(reg[0]),np.max(reg[1])
                res[val] = [(maxY-minY)/2,(maxX-minX)/2]
            ref.append(res)
        for x in listCandidate:
            lists = []
            coor_y = x[0]
            coor_x = x[1]
            for y in range (0,len(listGrowing)):
                # val = y[coor_y][coor_x]
                val = listGrowing[y][coor_y][coor_x]
                if val == 0:
                    continue
                lists.append(ref[y][val])
                # reg = (np.where(y == val))
                # minY,minX,maxY,maxX = np.min(reg[0]),np.min(reg[1]),np.max(reg[0]),np.max(reg[1])
                # lists.append([(maxY-minY)/2,(maxX-minX)/2])
            res = 0
            cnt = 0
            for x in range(0,len(lists)-1):
                sum = pow((lists[x][0]-lists[x+1][0]),2)+pow((lists[x][1]-lists[x+1][1]),2)
                res = res + np.sqrt(sum)
                cnt+=1
            if res != 0:
                res = res/cnt
            if  res > 1:
                truePixel.append([coor_y,coor_x])
            else :
                falsePixel.append([coor_y,coor_x])
        return truePixel,falsePixel

    # --------------------------------------------------

    def doFloodFill2(self, image,resImg ,is_visit, stack, regs, dataset, originalImage):
        res = []
        image = np.int_(image)
        self.threshold = colorDetection.getThreshold(self)
        clocks = c_data.clock(self)
        while len(stack) != 0:
            coory,coorx = stack[0]
            stack.pop(0)
            resImg[coory][coorx] = 255
            res.append(image[coory][coorx])
            data = originalImage[coory][coorx]
            B,G,R = data[0],data[1],data[2]
            for x in clocks:
                if  coory+x[0] < 0 or coory+x[0] == len(image) or coorx+x[1] < 0 or coorx+x[1] == len(image[0]) or is_visit[coory+x[0]][coorx+x[1]] != 0:
                    continue
                elif dataset[B][G][R] == True:
                    is_visit[coory+x[0]][coorx+x[1]] = regs
                    stack.append([coory+x[0],coorx+x[1]])
        return resImg,is_visit,res

    def getGrowingRegion2(self,list,images,dataset):
        grayImage = imageProcessing.toGray(self,images)
        is_visit = grayImage*0
        resImg = copy.copy(grayImage)
        region = 0
        for x in list:
            coor_y = x[0]
            coor_x = x[1]
            if is_visit[coor_y][coor_x] == 0:
                stack = []
                region+=1
                stack.append([coor_y,coor_x])
                is_visit[coor_y][coor_x] = region
                resImg, is_visit, res = self.doFloodFill2(grayImage,resImg,is_visit,stack,region,dataset, images)
        return is_visit
