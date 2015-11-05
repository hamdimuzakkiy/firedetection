__author__ = 'hamdiahmadi'
import video as vd
import moving as mv
import pixelDetection as pd
import classification as cls
import preprocessing2 as preprocessing
import wavelet as wv
import time
import copy
import numpy as np
import cv2
import luminance as lu

def readingVideo(videoFile):
    stdDev, mean = pd.getStdDevAndMean('../../corped/__ChoosenImage2')
    print "Stdev : "+str(stdDev), "Mean : "+str(mean)
    print "Video Frame : ",vd.countFrame(videoFile)
    print "Video Size : ",len(vd.readVideo(videoFile)[1]),len(vd.readVideo(videoFile)[1][0])
    counter = 0

    pdt = preprocessing.pixelDetection()
    idt = preprocessing.intensityDetection()
    classifier = cls.getClassification()
    ListHighPassWavelet = wv.setData()
    ListMap = lu.setData()
    while(vd.isOpened(videoFile)):
        try :
            #get curent frame
            currentFrame = vd.readVideo(videoFile)[1]

            # get moving pixel
            start1 = time.time()
            movingFrame = mv.getMovingForeGround(vd.copyFile(currentFrame))
            movingPixel = mv.getMovingPixel(vd.copyFile(movingFrame))

            #candidate pixel ( color probability )
            start2 = time.time()
            ListCandidatePixel = pdt.getCandidatePixel(movingPixel, currentFrame, stdDev, mean)
            candidatePixel = mv.delPixel(ListCandidatePixel[1], mv.getMovingForeGroundColor(currentFrame,movingFrame))

            #candidate pixel ( intensity threshold )
            gaussian7 = vd.getGaussian(vd.toGray(currentFrame),7)
            gaussian13 = vd.getGaussian(vd.toGray(currentFrame),13)
            gaussian = cv2.add((gaussian7/2),(gaussian13/2))

            #wavelet
            LL,(HL,LH,HH) = wv.toWavelet(vd.toGray(currentFrame))

            ListHighPassWavelet[counter%10] = [LH,HL,HH]
            ListMap[counter%10] = gaussian

            counter+=1
            if (counter < 10):
                continue

            # ListCandidatePixel2 = idt.getCandidatePixel2(ListMap,ListCandidatePixel[0])
            # ListCandidatePixel2 = idt.getCandidatePixel(gaussian,ListCandidatePixel[0])

            ListCandidatePixel2 = idt.getCandidatePixel2(gaussian,ListCandidatePixel[0])
            ListCandidatePixel3 = idt.getCandidatePixel3(ListMap,ListCandidatePixel2[0])
            candidatePixel2 = mv.delPixel(ListCandidatePixel3[1],mv.delPixel(ListCandidatePixel2[1], copy.copy(candidatePixel)))
            # print len(ListCandidatePixel[0]),len(ListCandidatePixel2[0])
            # ListFirePixel = cls.doClassification(classifier, ListCandidatePixel2[0], ListHighPassWavelet)

            print len(ListCandidatePixel[0]),len(ListCandidatePixel2[0]),len(ListCandidatePixel3[0])

            # d1 = cv2.pyrDown(currentFrame)
            # d2 = cv2.pyrDown(d1)
            # d3 = cv2.pyrDown(d2)
            # d4 = cv2.pyrDown(d3)
            # d5 = cv2.pyrDown(d4)
            # d6 = cv2.pyrDown(d5)
            #
            #
            # vd.showVideo("d6",d6)
            # print '==================',len(d6),len(d6[0]),'=================='
            # vd.showVideo("Gauss",gaussian)
            vd.showVideo("Moving",mv.getMovingForeGroundColor(currentFrame,movingFrame))
            vd.showVideo("Probability",candidatePixel)
            vd.showVideo("Intensity",candidatePixel2)
            vd.showVideo("Curent",currentFrame)

            # if (len(ListCandidatePixel[0])!=0):
            #     vd.saveFrame("aa/new"+str(counter)+'.png',candidatePixel)

            vd.waitVideo(1)
        except :
            return
    return

if __name__ == '__main__':
    fileName = '../../dataset/data2/flame1.avi'
    fileName = '../../dataset/uji/controlled2.avi'
    # fileName = '../../dataset/data1/smoke_or_flame_like_object_1.avi'
    fileName = '../../dataset/Automatic Fire detection using CCD Camera.mp4'
    # fileName = 0
    print fileName
    videoFile = vd.openVideo(fileName)
    start = time.time()
    res = readingVideo(videoFile)
    print time.time() - start
    vd.closeVideo(videoFile)