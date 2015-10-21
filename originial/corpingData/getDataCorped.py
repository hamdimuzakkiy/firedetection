__author__ = 'hamdiahmadi'
import video as vd
import moving as mv
import os
import wavelet as wv
import classification as cls
import numpy as np

def readingVideo(videoFile):
    counter=0
    classifier = cls.getClassification()
    global  videoName
    ListHighPassWavelet = wv.setData()
    if os.path.exists('../../../corpeds/'+videoName) == False :
        os.mkdir('../../../corpeds/'+videoName)
    while(vd.isOpened(videoFile) and counter != vd.countFrame(videoFile)-50):
        curentFrame = vd.readVideo(videoFile)[1]
        # movingFrame = mv.getMovingForeGround(curentFrame)

        LL,(HL,LH,HH) = wv.toWavelet(vd.toGray(curentFrame))

        ListHighPassWavelet[counter%10] = [HL,LH,HH]
        counter+=1
        if (counter<10):
            continue

        if (counter == 21):
            ListFirePixel = cls.doClassification(classifier, [[135,231]], ListHighPassWavelet)
            return

        # vd.saveFrame('../../../corpeds/'+videoName+'/'+str(a)+'.png',curentFrame)
        vd.waitVideo(1)

    return

if __name__ == '__main__':
    listDir = os.listdir('../../../dataset/data1')
    for i in listDir:
        if (i != 'smoke_or_flame_like_object_1.avi'):
            continue
        videoName = i
        fileName = '../../../dataset/data1/'+i
        videoFile = vd.openVideo(fileName)
        readingVideo(videoFile)
        vd.closeVideo(videoFile)
        break