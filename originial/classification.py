__author__ = 'hamdiahmadi'

import data as dt
import scipy
from sklearn import svm
import excel
import wavelet as wv
import numpy as np

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
            if abs(data[y]-data[y-1]) < 10:
               cnt+=1
        if (cnt > 1):
            flag = False

        if flag == True :
            print data
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
            data.append(y[x[0]][x[1]][2])
        print dt.getNormalRange(data)

    return res
