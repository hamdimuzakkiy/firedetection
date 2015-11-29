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
    truePixel = []
    falsePixel = []
    for x in list:
        data = []
        for y in wavelet:
            res = pow(y[0][x[0]][x[1]],2)+pow(y[1][x[0]][x[1]],2)+pow(y[2][x[0]][x[1]],2)
            result = float('%.2f' % res)
            data.append(result)
        data =  dt.getNormalRange2(data,wavelet[9])
        res = np.array(data)
        if len(np.where(res == 0)[0])<5:
            print data
            truePixel.append([x[0],x[1]])
        else :
            falsePixel.append([x[0],x[1]])
        # print data,np.std(data)
        # if np.std(data) > 0.1:
        #     truePixel.append([x[0],x[1]])
        # else :
        #     falsePixel.append([x[0],x[1]])
    return truePixel,falsePixel

def doClassification3(classifier, list, wavelet):
    for x in list:
        data = []
        LH = []
        HL = []
        HH = []
        for y in wavelet:
            LH.append(y[0][x[0]][x[1]])
            HL.append(y[1][x[0]][x[1]])
            HH.append(y[2][x[0]][x[1]])
        LH = dt.getNormalRange(LH)
        HL = dt.getNormalRange(HL)
        HH = dt.getNormalRange(HH)
        for y in range(0,len(LH)):
            data.append(pow(LH[y],2)+pow(HL[y],2)+pow(HH[y],2))
        print dt.getNormalRange(data),np.std(dt.getNormalRange(data))
        return