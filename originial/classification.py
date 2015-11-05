__author__ = 'hamdiahmadi'

import data as dt
import scipy
from sklearn import svm
import excel
import wavelet as wv

def readDataSet(file):
    data,classes = excel.readDataSet(file)
    return data, classes

def getClassification():
    x,y = readDataSet("waveletData/TA.xls")
    clf = svm.SVC(kernel = 'rbf',C = 1)
    clf.fit(x,y)
    return clf

def doClassification(classifier, list, wavelet):
    res = []
    for x in list:
        data = wv.getWaveletValue(x[0],x[1],wavelet)
        data,data2 = dt.getNormalRange(data)
        print data2
        # if (data[0] != 0):
            # print data,data2
            # res.append([x[0],x[1]])
        # if classifier.predict(data) == 'Api':
        #     res.append([x[0],x[1]])
        # else:
        #     pass
    return res
