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
        data = dt.getNormalRange(data)
        if classifier.predict(data) == 'Api':
            res.append([x[0],x[1]])
        else:
            pass
    return res

classifier = getClassification()
data = [0.382359758,	0.382359758,	0.455071496,	0.460072952,	0.576098384,	0.576098384,	0.577600367,	0.577600367	,0.785780043,	0.996120246]
print classifier.predict(data)