__author__ = 'hamdiahmadi'
import numpy as np
import sys
import cv2
import excel
import data as dt
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

    def getLumiananceImage(self,image):
        grayLuminance = imageProcessing.toGray(self,image)
        gaussianLuminance13 = imageProcessing.gaussianFilter(self,grayLuminance,13)
        gaussianLuminance7 = imageProcessing.gaussianFilter(self,grayLuminance,7)
        return self.toLuminance(gaussianLuminance7,gaussianLuminance13)

    def getLuminanceImageGray(self,image):
        grayLuminance = imageProcessing.toGray(self,image)
        gaussianLuminance13 = grayLuminance
        gaussianLuminance7 = grayLuminance
        return self.toLuminance(gaussianLuminance7,gaussianLuminance13)

    def localLuminance(self,image,listCandidate,Y,X):
        #other ways
        #arr = np.array(listCandidate)
        # minY,maxY =  min(arr[:,0]),max(arr[:,0])
        # minX,maxX =  min(arr[:,1]),max(arr[:,1])
        #end other ways

        truePixel =[]
        falsePixel=[]
        if (len(listCandidate) == 0):
            return truePixel,falsePixel
        # minY,maxY =  Y[0],Y[1]
        # minX,maxX =  X[0],X[1]
        # cnt = 0
        # sum = 0
        # for y in range (minY,maxY+1):
        #     for x in range(minX,maxX+1):
        #         sum+=image[y][x]
        #         cnt+=1
        # avg = float(sum)/float(cnt)
        avg = np.average(image)
        print '--',avg,'--'
        for x in listCandidate:
            coor_x = x[1]
            coor_y = x[0]
            if (avg <= image[coor_y][coor_x]):
                truePixel.append([coor_y,coor_x])
            else :
                falsePixel.append([coor_y,coor_x])
        return truePixel,falsePixel

    def luminanceNeighbour(self,image,listCandidate):
        clocks = c_data.clock(self)
        truePixel =[]
        falsePixel=[]
        for x in listCandidate:
            coor_x = x[1]
            coor_y = x[0]
            arr = []
            for y in clocks:
                if coor_y + y[0] < 0 or coor_y + y[0] > len(image)-1 or coor_x + y[1] < 0 or coor_x + y[1] > len(image[0])-1:
                    continue
                arr.append(image[coor_y+y[0]][coor_x+y[1]])
            arr.append(image[coor_y][coor_x])
            if np.average(arr)<=image[coor_y][coor_x]:
                truePixel.append([coor_y,coor_x])
            else :
                falsePixel.append([coor_y,coor_x])
        return truePixel,falsePixel

    def luminanceRemoval(self,listImage,listCandidate):
        truePixel = []
        falsePixel = []
        for x in listCandidate:
            list = []
            for y in listImage:
                sch = y[x[0]][x[1]]
                list.append(sch)
                lists = np.where(y == sch)
                list.append(len(lists[0]))
            std = np.std(list)
            if (std >= 5 and std <=40):
                truePixel.append([x[0],x[1]])
            else :
                falsePixel.append([x[0],x[1]])
            list = np.sort(list)
            results = c_data.getLuminanceDeviation(self,list)

            if (results>0.8):
                truePixel.append([x[0],x[1]])
            else :
                falsePixel.append([x[0],x[1]])
        return truePixel,falsePixel

class intensityDetection(c_data,colorDetection):

    def __init__(self):
        c_data.__init__(self)

    #candidate pixel based on average intensity picture
    def getIntensityPixel(self,image,listCandidate):
        truePixel = []
        falsePixel = []
        threshold = np.average(image)
        for x in listCandidate:
            if image[x[0]][x[1]] > threshold:
                truePixel.append([x[0],x[1]])
            else:
                falsePixel.append([x[0],x[1]])
        return truePixel,falsePixel

    #candidate pixel based on average intensity moving object with range 2* extrim point
    def getIntensityPixel3(self,image,listCandidate,range):
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
        # print minY,maxY,minX,maxX,len(image2),len(image2[0])
        threshold = np.average(image2)
        for x in listCandidate:
            if image[x[0]][x[1]] > threshold:
                truePixel.append([x[0],x[1]])
            else:
                falsePixel.append([x[0],x[1]])
        return truePixel,falsePixel

    def getIntensityPixel2(self,image,listCandidate):
        truePixel = []
        falsePixel = []
        if len(listCandidate) == 0:
            return truePixel,falsePixel
        listCandidate2 = np.array(copy.copy(listCandidate))

        minY,maxY =  min(listCandidate2[:,0]),max(listCandidate2[:,0])
        minX,maxX =  min(listCandidate2[:,1]),max(listCandidate2[:,1])

        if maxY*2>len(image):
            maxY = len(image)-1
        else:
            maxY = maxY*2
        if maxX*2>len(image):
            maxX = len(image)-1
        else:
            maxX = maxX*2
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

    #candidate pixel based on neighbour color
    def getCandidatePixel2(self,image,listCandidate):
        truePixel = []
        falsePixel = []
        clocks = c_data.clock(self)
        for x in listCandidate:
            coor_x = x[1]
            coor_y = x[0]
            arr = []
            for y in clocks:
                if coor_y + y[0] < 0 or coor_y + y[0] > len(image)-1 or coor_x + y[1] < 0 or coor_x + y[1] > len(image[0])-1:
                    continue
                arr.append(image[coor_y+y[0]][coor_x+y[1]])
            arr.append(image[coor_y][coor_x])
            dev = np.std(arr)
            if dev > 10 and dev < 20:
                truePixel.append([coor_y,coor_x])
            else :
                falsePixel.append([coor_y,coor_x])
        return truePixel,falsePixel

    #candidate pixel based on red chanel
    def getCandidatePixel4(self,listImage,listCandidate):
        truePixel = []
        falsePixel = []
        for x in listCandidate:
            arr = []
            for y in listImage:
                result = float('%.1f' % round(y[x[0]][x[1]], 2))
                arr.append(result)
        return truePixel,falsePixel

    def getCandidatePixel5(self,ListImage,listCandidate,stdDev, mean):
        truePixel = []
        falsePixel = []
        for x in listCandidate:
            arr = []
            cnt = 0
            for y in ListImage:
                arr.append([x[0]])
                arr.append([x[1]])
                if len(colorDetection.getCandidatePixel(self,arr,y,stdDev,mean)[0]) == 1:
                    cnt+=1

            if cnt > 1:
                truePixel.append([x[0],x[1]])
            else :
                falsePixel.append([x[0],x[1]])

        return truePixel,falsePixel

class wavelet(c_data):
    def __init__(self):
        pass

    def temporalAnalysis(self,ListImage,listCandidate):
        for x in listCandidate:
            arr = []
            coor_y,coor_x = x[0],x[1]
            for image in ListImage:
                arr.append(image[coor_y][coor_x][2])
            print arr

class growing(c_data):

    def __init__(self):
        self.threshold = 10

    def doGrowing(self,images ,imageGrowing,coor_y,coor_x):
        queue = []
        clocks = c_data.clock(self)
        queue.append([coor_y,coor_x])
        while len(queue)!=0:
            coor = queue.pop(0)
            coor_y,coor_x = coor[0],coor[1]
            val = images[coor_y][coor_x]
            for y in clocks:
                if coor_y + y[0] < 0 or coor_y + y[0] > len(images)-1 or coor_x + y[1] < 0 or coor_x + y[1] > len(images[0])-1:
                    pass
                elif imageGrowing[coor_y+y[0]][coor_x+y[1]] == 255:
                    pass
                elif abs(int(val)-int(images[coor_y+y[0]][coor_x+y[1]])) <= self.threshold:
                    imageGrowing[coor_y+y[0]][coor_x+y[1]] = 255
                    queue.append([coor_y+y[0],coor_x+y[1]])
        return imageGrowing

    def getGrowing(self,images,list):
        imageGrowing = copy.copy(images)
        imageGrowing = imageGrowing*0
        for x in list:
            coor_x = x[1]
            coor_y = x[0]
            print coor_y,coor_x,len(imageGrowing),len(imageGrowing[0])
            if imageGrowing[coor_y][coor_x] == 255:
                pass
            else:
                imageGrowing = self.doGrowing(copy.copy(images),copy.copy(imageGrowing),coor_y,coor_x)
        return imageGrowing