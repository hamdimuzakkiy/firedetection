from preprocessing2 import luminance

__author__ = 'hamdiahmadi'
import video as vd
import moving as mv
import pixelDetection as pd
import classification as cls
import preprocessing2 as preprocessing
import wavelet as wv
import time
import copy
import cv2
import numpy

def readingVideo(videoFile):
    stdDev, mean = pd.getStdDevAndMean('../../corped/__ChoosenImage2')
    print "Stdev : "+str(stdDev), "Mean : "+str(mean)
    print "Video Frame : ",vd.countFrame(videoFile)
    print "Video Size : ",len(vd.readVideo(videoFile)[1]),len(vd.readVideo(videoFile)[1][0])
    counter = 0

    cdt = preprocessing.colorDetection()
    idt = preprocessing.intensityDetection()
    lum = preprocessing.luminance()
    wvlt = preprocessing.wavelet()
    classifier = cls.getClassification()
    ListWavelet = []
    ListLuminance = []

    while(vd.isOpened(videoFile)):
        try :
            #get curent frame
            currentFrame = vd.readVideo(videoFile)[1]
            # currentFrame2 = vd.upSize(copy.copy(currentFrame))
            #compres image
            while (len(currentFrame)>150):
                if (len(currentFrame)<=300):
                    currentFrame2 = copy.copy(currentFrame)
                currentFrame = vd.downSize(currentFrame)

            # get moving pixel
            movingFrame = mv.getMovingForeGround(vd.copyFile(currentFrame))
            movingPixel = mv.getMovingPixel(vd.copyFile(movingFrame))

            #candidate pixel ( color probability )
            ListCandidatePixel = cdt.getCandidatePixel(movingPixel, currentFrame, stdDev, mean)

            #candidate pixel ( brightness ), convert image to gray with luminance
            luminanceImageGray = lum.getLuminanceImageGray(currentFrame)
            ListCandidatePixel = idt.getCandidatePixel(luminanceImageGray,ListCandidatePixel[0])

            # covert image to wavelet
            LL,(HL,LH,HH) = wv.toWavelet(vd.toGray(currentFrame2))
            #convert image to luminance image with gaussian filter 7 and 13
            luminanceImage = lum.getLumiananceImage(currentFrame)

            vd.saveFrame('temporary/LH.png',LH)
            vd.saveFrame('temporary/HL.png',HL)
            vd.saveFrame('temporary/HH.png',HH)

            LH = vd.readImage('temporary/LH.png')[:,:,2]
            HL = vd.readImage('temporary/HL.png')[:,:,2]
            HH = vd.readImage('temporary/HH.png')[:,:,2]

            #append image
            ListLuminance.append(luminanceImage)
            ListWavelet.append([HL,LH,HH])

            counter+=1
            if (counter<10):
                continue
            ListLuminance.pop(0)
            ListWavelet.pop(0)

            cls.doClassification2(classifier,ListCandidatePixel[0],ListWavelet)
            # ListCandidatePixel = idt.getCandidatePixel3(ListLuminance,ListCandidatePixel[0])

            vd.showVideo("luminanceImage",vd.upSize(luminanceImage))
            # vd.showVideo("luminanceImageFInal",vd.upSize(mv.markPixelBnW(ListCandidatePixel[0],luminanceImage)))
            vd.showVideo('Final',vd.upSize(vd.upSize(mv.markPixel(ListCandidatePixel[0],currentFrame))))
            # vd.showVideo('FinalLuminance',vd.upSize(vd.upSize(mv.markPixelBnW(ListCandidatePixel[0],luminanceImage))))
            vd.waitVideo(1)
        except:
            return
    return

if __name__ == '__main__':
    fileName = '../../dataset/data2/flame1.avi'
    fileName = '../../dataset/uji/fBackYardFire.avi'
    # fileName = '../../dataset/data3/IMG_7358.MOV'
    # fileName = '../../dataset/data1/smoke_or_flame_like_object_2.avi'
    # fileName = '../../dataset/Automatic Fire detection using CCD Camera.mp4'
    # fileName = 0

    print fileName
    videoFile = vd.openVideo(fileName)
    start = time.time()
    res = readingVideo(videoFile)
    print time.time() - start
    vd.closeVideo(videoFile)