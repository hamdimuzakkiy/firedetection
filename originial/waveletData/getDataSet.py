__author__ = 'hamdiahmadi'

import video as vd
import wavelet as wv
import numpy as np
import excel
import data as dt

def readingVideo(videoFile,start,countFrame,coory,coorx):
    res = []
    frameCounter = 0
    while vd.isOpened(videoFile):
        try:
            if frameCounter >= start :
                LL,(HL,LH,HH) = wv.toWavelet(vd.toGray(vd.readVideo(videoFile)[1]))
                newCoory = coory/2
                newCoorx = coorx/2
                res.extend([np.power(LH[newCoory][newCoorx],2)+np.power(HL[newCoory][newCoorx],2)+np.power(HH[newCoory][newCoorx],2)])
            frameCounter+=1
            if frameCounter == start+countFrame:
                return res
        except :
            print "Wrong"
            return res

# def getNormalRange(data):
#     max = np.max(data)
#     res = np.sort(data/max)
#     return res
excelFile = 'TA.xls'
StoreDataSet = excel.retriveListDataset(excelFile)

for x in StoreDataSet:
    videoFile = vd.openVideo('../'+x[0])
    res = readingVideo(videoFile,float(x[3]),10,float(x[1]),float(x[2]))
    print x,res,float(x[3]),float(x[1]),float(x[2])
    res = dt.getNormalRange(res)
    excel.saveDataSet('TA.xls',res,x[4])
# coory,coorx = 96, 193
# start = 0
# countFrame = 10
# fileName = '../../dataset/data2/flame1.avi'
# classes = "Api"
# videoFile = vd.openVideo(fileName)
# res = readingVideo(videoFile,start,countFrame,coory,coorx)
# max = np.max(res)
# res = np.sort(res/max)
# excel.saveDataSet('TA.xls',res,classes)
