__author__ = 'hamdiahmadi'
import numpy as np
import cv2
import excel
import data as dt

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

class pixelDetection(c_data):

    def __init__(self):
        c_data.__init__(self)
        self.threshold = pow(10,-8)

    def getCandidatePixel(self,list, image, stdDev, mean):
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


class intensityDetection(c_data):

    def __init__(self):
        c_data.__init__(self)

    #candidate pixel based on std dev picture
    def getCandidatePixel(self,image,listCandidate):
        truePixel = []
        falsePixel = []
        threshold = np.std(image)
        for x in listCandidate:
            if image[x[0]][x[1]] > threshold:
                truePixel.append([x[0],x[1]])
            else:
                falsePixel.append([x[0],x[1]])
        return truePixel,falsePixel

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

    #candidate pixel based on neighbour color
    def getCandidatePixel2(self,image,listCandidate):
        truePixel = []
        falsePixel = []
        clocks = self.clock()
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
            res = float(np.std(arr))
            arr = np.sort(arr)
            if (res > 5 and res < 40):
                # print res
                cnt = 0
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
