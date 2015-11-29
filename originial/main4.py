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

def get_user_input(user_input_ref):
    user_input_ref[0] = raw_input("Give me some Information: ")

def readingVideo(videoFile):
    stdDev, mean = pd.getStdDevAndMean('__ChoosenImage2')
    print "Stdev : "+str(stdDev), "Mean : "+str(mean)
    print "Video Frame : ",vd.countFrame(videoFile)
    print "Video Size : ",len(vd.readVideo(videoFile)[1]),len(vd.readVideo(videoFile)[1][0])

    counter = 0
    cdt = preprocessing.colorDetection()
    idt = preprocessing.intensityDetection()
    lum = preprocessing.luminance()
    grow = preprocessing.growing()
    wvlt = preprocessing.wavelet()
    classifier = cls.getClassification()
    fireFrame = numpy.array([0,0,0,0,0])
    ListWavelet = []
    ListLuminance = []
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
            ColorCandidatePixel = cdt.getCandidatePixel(copy.copy(movingPixel), currentFrame, stdDev, mean)

            #candidate pixel ( brightness ), convert image to gray with luminance
            luminanceImageGray = lum.getLuminanceImageGray(currentFrame)
            LuminanceCandidatePixel = idt.getIntensityPixel3(luminanceImageGray,copy.copy(ColorCandidatePixel[0]),copy.copy(movingPixel))

            # covert image to wavelet
            LL,(HL,LH,HH) = wv.toWavelet(vd.toGray(currentFrame2))
            #convert image to luminance image with gaussian filter 7 and 13
            luminanceImage = lum.getLumiananceImage(currentFrame)

            vd.saveFrame('temporary/LH.png',LH)
            vd.saveFrame('temporary/HL.png',HL)
            vd.saveFrame('temporary/HH.png',HH)

            LH = vd.readImage('temporary/LH.png')
            HL = vd.readImage('temporary/HL.png')
            HH = vd.readImage('temporary/HH.png')

            LH = LH[:,:,2]
            HL = HL[:,:,2]
            HH = HH[:,:,2]

            #append image
            ListLuminance.append(luminanceImage)
            ListWavelet.append([HL,LH,HH])

            counter+=1
            if (counter<=10):
                continue
            ListLuminance.pop(0)
            ListWavelet.pop(0)

            ListCandidatePixel = idt.getDiferencePixel(ListLuminance,copy.copy(LuminanceCandidatePixel[0]))

            # newImage = grow.getGrowing(luminanceImage,ListCandidatePixel[0])
            # vd.saveFrame('temporary/'+str(counter)+'.png',newImage)
            # vd.showVideo('Luminance',vd.upSize(luminanceImage))
            # FinalCandidatePixel = cls.doClassification2(classifier,ListCandidatePixel[0],ListWavelet)

            if len(movingPixel[0])>0:
                fireFrame[0]+=1
            if len(ColorCandidatePixel[0])>0:
                fireFrame[1]+=1
            if len(LuminanceCandidatePixel[0])>0:
                fireFrame[2]+=1
            if len(ListCandidatePixel[0])>0:
                fireFrame[3]+=1
            # if len(FinalCandidatePixel[0])>0:
            #     fireFrame[4]+=1
            AllFrame+=1

            # print len(movingPixel[0]),len(ColorCandidatePixel[0]),len(LuminanceCandidatePixel[0]),len(ListCandidatePixel[0])

            fireFrameImage = vd.upSize(vd.upSize(mv.markPixelRectangle(ListCandidatePixel[0],currentFrame)))
            vd.showVideo('Final',fireFrameImage)
            # vd.showVideo('Final',vd.upSize(mv.markPixelRectangleBnW(ListCandidatePixel[0],luminanceImage)))
            vd.waitVideo(1)
        except :
            print fireFrame,AllFrame
            return (fireFrame)/float(AllFrame)
    print fireFrame,AllFrame
    return (fireFrame)/float(AllFrame)


if __name__ == '__main__':
    fileName = '../../dataset/data2/flame1.avi'
    fileName = '../../dataset/uji/fBackYardFire.avi'
    # fileName = '../../dataset/data3/IMG_7357.MOV'
    # fileName = '../../dataset/data1/smoke_or_flame_like_object_3.avi'
    # fileName = '../../dataset/Automatic Fire detection using CCD Camera.mp4'
    # fileName = 0

    print fileName
    videoFile = vd.openVideo(fileName)
    start = time.time()
    res = readingVideo(videoFile)
    print time.time() - start
    print "Acc : ",res*100,' %'
    vd.closeVideo(videoFile)