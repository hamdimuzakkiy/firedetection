__author__ = 'hamdiahmadi'

import scipy
from sklearn import svm
import excel
import numpy as np
import copy

def readDataSet(file):
    data,classes = excel.readDataSet(file)
    return data, classes

def getClassifier(datatraining):
    x,y = readDataSet(datatraining)
    clf = svm.SVC(kernel = 'rbf',C = 5)
    clf.fit(x,y)
    return clf

def doClassification(classifier, list, wavelet):
    truePixel = []
    falsePixel = []
    listMax = []
    listMin = []
    cpyWavelet = np.int_(copy.copy(wavelet))
    cpyWavelet = np.power(cpyWavelet,2)
    for x in cpyWavelet:
        lists = np.add(np.add(x[0],x[1]),x[2])
        listMax.append(np.max(lists))
        listMin.append(np.min(lists))
    for x in list:
        data = []
        cnt= 0
        for y in wavelet:
            res = pow(y[0][x[0]][x[1]],2)+pow(y[1][x[0]][x[1]],2)+pow(y[2][x[0]][x[1]],2)
            res = (float(res)-float(listMin[cnt]))/(float(listMax[cnt])-float(listMin[cnt]))
            res = float('%.2f' % res)
            cnt+=1
            data.append(res)
        data = np.sort(data)
        classes = classifier.predict(data)
        if classes == 'Api':
            truePixel.append([x[0],x[1]])
        else :
            falsePixel.append([x[0],x[1]])
    return truePixel,falsePixel

def returnDataTraining(list, wavelet):
    listMax = []
    listMin = []
    result = []
    cpyWavelet = np.int_(copy.copy(wavelet))
    cpyWavelet = np.power(cpyWavelet,2)
    for x in cpyWavelet:
        lists = np.add(np.add(x[0],x[1]),x[2])
        listMax.append(np.max(lists))
        listMin.append(np.min(lists))
    for x in list:
        data = []
        cnt= 0
        for y in wavelet:
                res = pow(y[0][x[0]][x[1]],2)+pow(y[1][x[0]][x[1]],2)+pow(y[2][x[0]][x[1]],2)
                res = (float(res)-float(listMin[cnt]))/(float(listMax[cnt])-float(listMin[cnt]))
                res = float('%.2f' % res)
                cnt+=1
                data.append(res)
        data = np.sort(data)
        result.append(data)
    return result