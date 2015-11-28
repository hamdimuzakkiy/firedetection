__author__ = 'hamdiahmadi'

import data as dt
import scipy
from sklearn import svm
import excel
import wavelet as wv
import numpy as np
import cv2

def readDataSet(file):
    data,classes = excel.readDataSet(file)
    return data, classes

def getClassification():
    x,y = readDataSet("waveletData/TA.xls")
    clf = svm.SVC(kernel = 'rbf',C = 1)
    clf.fit(x,y)
    return clf

def doClassification(classifier, list, wavelet):
    truePixel = []
    falsePixel = []
    flag = True

    for x in list:
        data = wv.getWaveletValue(x[0],x[1],wavelet)
        cnt = 0
        for y in range(1,len(data)):
            if abs(data[y]-data[y-1]) >= 0 and abs(data[y]-data[y-1]) <= (min(data[y],data[y-1])*0.1):
               cnt+=1
        if (cnt > 4):
            flag = False
        # print data,cnt
        if flag == True :
            # print np.sort(data),np.mean(data)
            truePixel.append([x[0],x[1]])
        else :
            falsePixel.append([x[0],x[1]])
    return truePixel,falsePixel
        # if classifier.predict(data) == 'Api':
        #     res.append([x[0],x[1]])
        # else:
        #     pass
    # return res


def doClassification2(classifier, list, wavelet):
    res = []
    for x in list:
        data = []
        for y in wavelet:
            # data.append(y[x[0]][x[1]][2])
            # print len(y),len(y[0])
            # print x[0],x[1]
            res = pow(y[0][x[0]][x[1]],2)+pow(y[1][x[0]][x[1]],2)+pow(y[2][x[0]][x[1]],2)
            result = float('%.1f' % round(res, 2))
            data.append(res)

        print np.sort(dt.getNormalRange(data))

    return res

def doClassification3(list,counter):
    baseLH = 'wv/LH2/'
    baseHL = 'wv/HL2/'
    baseHH = 'wv/HH2/'
    wavelet = []

    for x in range (counter-9,counter+1):

        LH = cv2.imread(baseLH+str(x)+'.png')
        HL = cv2.imread(baseHL+str(x)+'.png')
        HH = cv2.imread(baseHH+str(x)+'.png')
        wavelet.append([LH,HL,HH])
    for x in list:
        coor_x = x[1]
        coor_y = x[0]
        data = []
        for y in wavelet:
            res = pow(y[0][coor_y][coor_x][0],2)+pow(y[1][coor_y][coor_x][0],2)+pow(y[2][coor_y][coor_x][0],2)
            data.append(res)
        print np.sort(data)
    return 1
