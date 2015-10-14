__author__ = 'hamdiahmadi'
import video as vd
import wavelet as wv
import numpy as np

def readingVideo(videoFile,start,countFrame,coory,coorx):
    res = []
    frameCounter = 0
    while vd.isOpened(videoFile):
        try:
            if frameCounter >= start :
                LL,(HL,LH,HH) = wv.toWavelet(vd.toGray(vd.readVideo(videoFile)[1]))
                # print len(HH),len(HH[0]),'---',len(vd.readVideo(videoFile)[1]),len(vd.readVideo(videoFile)[1][0])
                newCoory = coory/2
                newCoorx = coorx/2
                print LH[newCoory][newCoorx],HL[newCoory][newCoorx],HH[newCoory][newCoorx]
                res.append([np.power(LH[newCoory][newCoorx],2)+np.power(HL[newCoory][newCoorx],2)+np.power(HH[newCoory][newCoorx],2)])
            frameCounter+=1
            if frameCounter == start+countFrame:
                return res
        except :
            return res

coory,coorx = 205, 185
start = 0
countFrame = 10
fileName = '../../dataset/data2/flame1.avi'
videoFile = vd.openVideo(fileName)
res = readingVideo(videoFile,start,countFrame,coory,coorx)
for x in res:
    print x[0]