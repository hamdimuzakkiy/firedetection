__author__ = 'hamdiahmadi'
import numpy as np
import sys
import cv2
import excel
import data as dt
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
            res.append(tmp)
        return res

class colorDetection(c_data):

    def __init__(self):
        c_data.__init__(self)

    def getCandidatePixel(self,list, image, stdDev, mean):
        self.threshold = pow(10,-8)
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
            print image[coor_y][coor_x]
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
            print results
            if (results>0.8):
                truePixel.append([x[0],x[1]])
            else :
                falsePixel.append([x[0],x[1]])
        return truePixel,falsePixel


class intensityDetection(c_data,colorDetection):

    def __init__(self):
        c_data.__init__(self)

    #candidate pixel based on std dev picture
    def getCandidatePixel(self,image,listCandidate):
        truePixel = []
        falsePixel = []
        # threshold = np.std(image)
        threshold = np.average(image)
        for x in listCandidate:
            if image[x[0]][x[1]] > threshold:
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

    #candidate pixel based on x,y pixel with 10 frame
    def getCandidatePixel3(self,listImage,listCandidate):
        truePixel = []
        falsePixel = []
        for x in listCandidate:
            arr = []
            for y in listImage:
                arr.append(y[x[0]][x[1]])
            # arr = c_data.getNormalRange(self,arr)
            res = float(np.std(arr))
            print res, arr
            if (res > 5 and res < 20):
                truePixel.append([x[0],x[1]])
                continue
                # for y in range(1,len(arr)) :
                #     if (int(arr[y])-int(arr[y-1])==0):
                #         cnt+=1
                # if cnt <= 0:
                #     truePixel.append([x[0],x[1]])
                # else :
                #     falsePixel.append([x[0],x[1]])
            else:
                falsePixel.append([x[0],x[1]])

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
            print arr
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