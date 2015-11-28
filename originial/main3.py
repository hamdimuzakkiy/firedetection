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

    pdt = preprocessing.pixelDetection()
    idt = preprocessing.intensityDetection()
    lum = preprocessing.luminance()
    wvlt = preprocessing.wavelet()
    classifier = cls.getClassification()
    ListWavelet = []
    ListMap = []
    ListOriginal = []
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
            ListCandidatePixel = pdt.getCandidatePixel(movingPixel, currentFrame, stdDev, mean)
            candidatePixel = mv.delPixel(ListCandidatePixel[1], mv.getMovingForeGroundColor(currentFrame,movingFrame))

            # gray = vd.toGray(currentFrame)
            # grayLuminance = vd.toGray(currentFrame3)
            # gaussianLuminance13 = vd.getGaussian(grayLuminance,13)
            # gaussianLuminance7 = vd.getGaussian(grayLuminance,7)
            #get max and min image , normalization image
            # max7,max13 = numpy.max(gaussianLuminance7),numpy.max(gaussianLuminance13)
            # min7,min13 = numpy.min(gaussianLuminance7),numpy.min(gaussianLuminance13)
            # gaussianLuminance7-=min7
            # gaussianLuminance13-=min13
            # gaussianLuminance7*=(255/(max7-min7))
            # gaussianLuminance13*=(255/(max13-min13))
            # gaussians = cv2.add((gaussianLuminance7),(gaussianLuminance13))
            # gaussians = cv2.GaussianBlur(cv2.pyrUp(gaussians),(5,5),0)


            #wavelet
            # LL,(HL,LH,HH) = wv.toWavelet(vd.getGaussian(vd.toGray(currentFrame2),7))
            # LL,(HL,LH,HH) = wv.toWavelet(cv2.cvtColor(currentFrame2,cv2.COLOR_BGR2YUV)[:,:,0])

            # ListWavelet.append([LH,HL,HH])
            # ListMap.append(gray)
            # ListOriginal.append(currentFrame)

            # ListLuminance.append(gaussians)
            ListOriginal.append(currentFrame)
            counter+=1
            if (counter <= 10):
                continue
            ListOriginal.pop(0)
            # ListWavelet.pop(0)
            # ListFirePixel = cls.doClassification2(classifier, ListCandidatePixel[0], ListWavelet)
            vd.showVideo("Final",currentFrame)
            wvlt.temporalAnalysis(ListOriginal,ListCandidatePixel[0])

            # ListMap.pop(0)
            # ListOriginal.pop(0)
            # ListLuminance.pop(0)
            # if (len(movingPixel[0])!=0):
            #     X = min(movingPixel[1]),max(movingPixel[1])
            #     Y = min(movingPixel[0]),max(movingPixel[0])
            # else :
            #     X = 0,0
            #     Y = 0,0
            # ListCandidatePixel0 = lum.localLuminance(gaussians,ListCandidatePixel[0],Y,X)
            # localLuminance = mv.markPixel(ListCandidatePixel0[0],currentFrame)
            # vd.showVideo("local luminance",localLuminance)
            # vd.showVideo("luminance",gaussians)
            # ListCandidatePixel0 = lum.luminanceRemoval(ListLuminance,copy.copy(ListCandidatePixel[0]))
            # print len(ListCandidatePixel[0]),len(ListCandidatePixel0[0])


            vd.waitVideo(1)
        except ValueError:
            return
    return

if __name__ == '__main__':
    fileName = '../../dataset/data2/flame1.avi'
    # fileName = '../../dataset/uji/Man on Fire Building Jump - 9 Story Drop of Doom.mp4'
    # fileName = '../../dataset/data3/IMG_7358.MOV'
    # fileName = '../../dataset/data1/smoke_or_flame_like_object_1.avi'
    # fileName = '../../dataset/Automatic Fire detection using CCD Camera.mp4'
    # fileName = 0

    print fileName
    videoFile = vd.openVideo(fileName)
    start = time.time()
    res = readingVideo(videoFile)
    print time.time() - start
    vd.closeVideo(videoFile)