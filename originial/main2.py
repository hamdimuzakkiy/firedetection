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
    ListWavelet = []
    ListMap = []
    # ListMap = lu.setData()
    ListOriginal = lu.setData()
    while(vd.isOpened(videoFile)):
        try :
            #get curent frame
            currentFrame = vd.readVideo(videoFile)[1]
            #compres image

            while (len(currentFrame)>150):
                if (len(currentFrame)<=300):
                    currentFrame2 = copy.copy(currentFrame)
                currentFrame = cv2.pyrDown(currentFrame)

            # get moving pixel
            movingFrame = mv.getMovingForeGround(vd.copyFile(currentFrame))
            movingPixel = mv.getMovingPixel(vd.copyFile(movingFrame))

            #candidate pixel ( color probability )
            ListCandidatePixel = pdt.getCandidatePixel(movingPixel, currentFrame, stdDev, mean)
            candidatePixel = mv.delPixel(ListCandidatePixel[1], mv.getMovingForeGroundColor(currentFrame,movingFrame))

            #candidate pixel ( intensity threshold )
            gray = vd.toGray(currentFrame)
            # gaussian = vd.getGaussian(vd.toGray(currentFrame),7)
            gaussian13 = vd.getGaussian(gray,7)
            # gaussian = cv2.add((gaussian7/2),(gaussian13/2))

            #wavelet
            LL,(HL,LH,HH) = wv.toWavelet(vd.toGray((currentFrame2)))
            ListWavelet.append([LH,HL,HH])
            ListMap.append(gray)

            counter+=1
            if (counter <= 10):
                continue

            ListWavelet.pop(0)
            ListMap.pop(0)
            ListCandidatePixel1 = idt.getCandidatePixel(gaussian13,ListCandidatePixel[0])
            candidatePixel1 = mv.delPixel(ListCandidatePixel1[1], copy.copy(candidatePixel))

            # vd.showVideo("Candidate 1",cv2.pyrUp(cv2.pyrUp(candidatePixel1)))

            ListCandidatePixel2 = ListCandidatePixel1
            ListCandidatePixel3 = idt.getCandidatePixel3(ListMap,ListCandidatePixel2[0])
            candidatePixel3 = mv.delPixel(ListCandidatePixel3[1],mv.delPixel(ListCandidatePixel2[1], copy.copy(candidatePixel1)))
            # candidatePixel3 = mv.markPixel(ListCandidatePixel3[0],currentFrame)

            # vd.showVideo("Candidate 2",cv2.pyrUp(cv2.pyrUp(candidatePixel3)))

            ListFirePixel = cls.doClassification(classifier, ListCandidatePixel3[0], ListWavelet)
            candidatePixel4 = mv.delPixel(ListFirePixel[1],candidatePixel3)
            finalPixel3 = mv.markPixel(ListFirePixel[0],currentFrame)

            # vd.showVideo("Gray",((gaussian13)))
            # vd.showVideo("Real",(currentFrame))
            vd.showVideo("Final Candidate Black",(cv2.pyrUp(candidatePixel4)))
            vd.showVideo("Final Candidate",cv2.pyrUp(cv2.pyrUp(finalPixel3)))
            # vd.showVideo("Color",(candidatePixel))
            # vd.showVideo("Moving",(movingFrame))


            vd.waitVideo(1)
        except:
            return
    return

if __name__ == '__main__':
    fileName = '../../dataset/data2/flame1.avi'
    fileName = '../../dataset/uji/Man on Fire Building Jump - 9 Story Drop of Doom.mp4'
    fileName = '../../dataset/data3/IMG_7358.MOV'
    # fileName = '../../dataset/data1/smoke_or_flame_like_object_1.avi'
    # fileName = '../../dataset/11969485_10156181325945434_1774756015_n.mp4'
    # fileName = 0

    print fileName
    videoFile = vd.openVideo(fileName)
    start = time.time()
    res = readingVideo(videoFile)
    print time.time() - start
    vd.closeVideo(videoFile)