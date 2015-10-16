__author__ = 'hamdiahmadi'

import data as dt
import scipy
from sklearn import svm
import excel
import wavelet as wv

def readDataSet(file):
    data,classes = excel.readDataSet(file)
    cnt = 0
    # for x in data:
    #     print x,classes[cnt]
    return data, classes

def getClassification():
    x,y = readDataSet("TA.xls")
    clf = svm.SVC(kernel = 'rbf', C = 1)
    clf.fit(x,y)
    return clf

def doClassification(classifier, list, wavelet):
    res = []
    for x in list:
        data = wv.getWaveletValue(x[0],x[1],wavelet)
        data = dt.getNormalRange(data)
        if classifier.predict(data) == 'Api':
            res.append([x[0],x[1]])
    return res

# x,y = readDataSet("TA.xls")
# clf = svm.SVC(kernel = 'rbf', C = 1)
# clf.fit(x,y)
# print clf
# clf = getClassification()
# print clf.predict([[0.03663407455919139, 0.04657177912206545, 0.062031847646914585, 0.16250535897112167, 0.17991165890772148, 0.1882841180547626, 0.2993785600281797, 0.5343816358487037, 0.5358403952233247, 1.0]])
# x = [[1,2,4],[5,8,1],[2,1.5,1.8],[1,8,8],[3,1,0.6],[11,9,11]]
# y = ["Api","Bukan Api","Api","Bukan Api","Api","Bukan Api"]

# print clf.predict([[6,0,2]])