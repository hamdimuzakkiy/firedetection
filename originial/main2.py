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
    ListWavelet = wv.setData()
    ListMap = lu.setData()
    ListOriginal = lu.setData()
    while(vd.isOpened(videoFile)):
        try :
            #get curent frame
            currentFrame = vd.readVideo(videoFile)[1]
            real = copy.copy(currentFrame)


            while (len(currentFrame)>150):
                if (len(currentFrame)<=300):
                    currentFrame2 = copy.copy(currentFrame)
                currentFrame = cv2.pyrDown(currentFrame)

            # currentFrame2[:,:,1] = 0
            # currentFrame2[:,:,0] = 0

            # yspace = cv2.cvtColor(currentFrame,cv2.COLOR_BGR2YUV)
            #
            # movingFrame = mv.getMovingForeGround(vd.copyFile(yspace))
            # movingPixel = mv.getMovingPixel(vd.copyFile(movingFrame))
            # video = mv.getMovingForeGroundColor(yspace,movingFrame)
            # vd.showVideo("hamdi",video)
            # vd.waitVideo(1)
            # continue

            # get moving pixel
            movingFrame = mv.getMovingForeGround(vd.copyFile(currentFrame))
            movingPixel = mv.getMovingPixel(vd.copyFile(movingFrame))

            #candidate pixel ( color probability )
            ListCandidatePixel = pdt.getCandidatePixel(movingPixel, currentFrame, stdDev, mean)
            candidatePixel = mv.delPixel(ListCandidatePixel[1], mv.getMovingForeGroundColor(currentFrame,movingFrame))

            #candidate pixel ( intensity threshold )
            gray = vd.toGray(currentFrame)
            gaussian1 = vd.getGaussian(vd.toGray(currentFrame),1)
            gaussian13 = vd.getGaussian(gray,13)
            # gaussian = cv2.add((gaussian7/2),(gaussian13/2))

            #wavelet
            LL,(HL,LH,HH) = wv.toWavelet(vd.toGray((currentFrame2)))

            ListWavelet[counter%10] = [LH,HL,HH]
            # ListWavelet[counter%10] = [vd.toGray(currentFrame2),vd.toGray(currentFrame2),vd.toGray(currentFrame2)]
            ListMap[counter%10] = gray
            ListOriginal[counter%10] = currentFrame

            counter+=1
            if (counter < 10):
                continue

            ListCandidatePixel1 = idt.getCandidatePixel(gaussian13,ListCandidatePixel[0])
            candidatePixel1 = mv.delPixel(ListCandidatePixel1[1],mv.delPixel(ListCandidatePixel1[1], copy.copy(candidatePixel)))

            ListCandidatePixel2 = idt.getCandidatePixel2(gaussian1,ListCandidatePixel1[0])
            # ListCandidatePixel2 = ListCandidatePixel1
            ListCandidatePixel3 = idt.getCandidatePixel3(ListMap,ListCandidatePixel2[0])

            candidatePixel2 = mv.delPixel(ListCandidatePixel3[1],mv.delPixel(ListCandidatePixel2[1], copy.copy(candidatePixel1)))

            if (len(ListCandidatePixel3[0])!=0):
                print "Counter "+str(counter)+" : ",counter,len(movingPixel[0]),len(ListCandidatePixel[0]),len(ListCandidatePixel1[0]),len(ListCandidatePixel2[0]),len(ListCandidatePixel3[0])
                print "--------------------------"

            ListFirePixel = cls.doClassification(classifier, ListCandidatePixel3[0], ListWavelet)

            # vd.showVideo("Gray",((gaussian13)))
            vd.showVideo("Real",(currentFrame))
            vd.showVideo("Final Candidate",((candidatePixel2)))
            # vd.showVideo("Candidate",(candidatePixel1))
            vd.showVideo("Color",(candidatePixel))
            # vd.showVideo("Moving",(movingFrame))
            # if (len(ListCandidatePixel[0])!=0):
            #     vd.saveFrame("aa/new"+str(counter)+'.png',candidatePixel)

            vd.waitVideo(1)
        except :
            return
    return

if __name__ == '__main__':
    fileName = '../../dataset/data2/flame1.avi'
    # fileName = '../../dataset/uji/barbeq.avi'
    # fileName = '../../dataset/data3/IMG_7358.MOV'
    fileName = '../../dataset/data1/smoke_or_flame_like_object_1.avi'
    # fileName = '../../dataset/Red Velvet - Dumb Dumb Dance Compilation [Mirrored].mp4'
    fileName = 0
    print fileName
    videoFile = vd.openVideo(fileName)
    start = time.time()
    res = readingVideo(videoFile)
    print time.time() - start
    vd.closeVideo(videoFile)