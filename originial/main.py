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
import numpy

user_input = [None]

def readingVideo(videoFile):
    stdDev, mean = pd.getStdDevAndMean('__ChoosenImage2')
    print "Stdev : "+str(stdDev), "Mean : "+str(mean)
    print "Video Frame : ",vd.countFrame(videoFile)
    print "Video Size : ",len(vd.readVideo(videoFile)[1]),len(vd.readVideo(videoFile)[1][0])

    counter = 0
    cdt = preprocessing.colorDetection()
    idt = preprocessing.intensityDetection()
    lum = preprocessing.luminance()
    grw = preprocessing.growing()

    classifier = cls.getClassification()
    fireFrame = numpy.array([0,0,0,0,0])
    ListWavelet = []
    ListLuminance = []
    ListGrayImage = []
    AllFrame = 0

    while(vd.isOpened(videoFile)):
        try :
            #get curent frame
            currentFrame = vd.readVideo(videoFile)[1]
            #compres image
            while (len(currentFrame)>150):
                if (len(currentFrame)<=300):
                    currentFrame2 = copy.copy(currentFrame)
                currentFrame = vd.downSize(currentFrame)

            # get moving pixel
            movingFrame = mv.getMovingForeGround(vd.copyFile(currentFrame))
            movingPixel = mv.getMovingPixel(vd.copyFile(movingFrame))

            #candidate pixel ( color probability )
            ColorCandidatePixel = cdt.getCandidatePixel(copy.copy(movingPixel), copy.copy(currentFrame), stdDev, mean)

            #candidate pixel ( brightness ), convert image to gray with luminance
            luminanceImageGray = lum.getLuminanceImageGray(copy.copy(currentFrame))
            LuminanceCandidatePixel = idt.getIntensityPixel(copy.copy(luminanceImageGray),copy.copy(ColorCandidatePixel[0]),copy.copy(movingPixel))

            #convert image to luminance image with gaussian filter 7 and 13
            luminanceImage = lum.getLumiananceImage(currentFrame)

            # covert image to wavelet
            grayImage = vd.toGray(currentFrame2)
            LL,(HL,LH,HH) = wv.toWavelet(copy.copy(grayImage))

            ListGrowPixel = grw.getRegion(LuminanceCandidatePixel[0],copy.copy(currentFrame),stdDev, mean,counter)

            #append image
            ListLuminance.append(luminanceImage)
            ListWavelet.append([HL,LH,HH])
            ListGrayImage.append(copy.copy(grayImage))

            counter+=1
            if (counter<=10):
                continue

            ListLuminance.pop(0)
            ListWavelet.pop(0)
            ListGrayImage.pop(0)

            # ListCandidatePixel = idt.getDiferencePixel(ListLuminance,copy.copy(LuminanceCandidatePixel[0]))
            # ListCandidatePixel = copy.copy(LuminanceCandidatePixel)
            FinalCandidatePixel = cls.doClassification(classifier,copy.copy(ListGrowPixel[0]),ListWavelet)
            # cls.doClassification(classifier,copy.copy(ListCandidatePixel[0]),ListWavelet)

            if len(movingPixel[0])>0:
                fireFrame[0]+=1
            if len(ColorCandidatePixel[0])>0:
                fireFrame[1]+=1
            if len(LuminanceCandidatePixel[0])>0:
                fireFrame[2]+=1
            if len(ListGrowPixel[0])>0:
                fireFrame[3]+=1
            if len(FinalCandidatePixel[0])>0:
                fireFrame[4]+=1
            AllFrame+=1

            fireFrameImage = vd.upSize(vd.upSize(mv.markPixelRectangle(FinalCandidatePixel[0],currentFrame)))
            vd.showVideo('Final',fireFrameImage)
            vd.waitVideo(1)
        except:
            return (fireFrame)/float(AllFrame)
    return (fireFrame)/float(AllFrame)


if __name__ == '__main__':
    fileName = '../../dataset/data2/flame3.avi'
    fileName = '../../dataset/uji/TunnelAccident3.avi'
    # fileName = '../../dataset/data3/IMG_7357.MOV'
    # fileName = '../../dataset/data1/smoke_or_flame_like_object_3.avi'
    # fileName = '../../dataset/Automatic Fire detection using CCD Camera.mp4'
    # fileName = 0

    print fileName
    videoFile = vd.openVideo(fileName)
    start = time.time()
    res = readingVideo(videoFile)
    print "Time : ",time.time() - start
    print "Acc : ",res*100,' %'
    vd.closeVideo(videoFile)