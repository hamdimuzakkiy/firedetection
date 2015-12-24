__author__ = 'hamdiahmadi'
import classification as cls

import excel
import moving as mv
import preprocessing as preprocessing
import wavelet as wv
import time
import copy
import numpy


def readingVideo(videoFile):
    Color = preprocessing.ColorDetection()
    File = preprocessing.File()
    RegionGrowing = preprocessing.RegionGrowing()
    ImageProcessing = preprocessing.ImageProcessing()
    Moving = preprocessing.Moving()

    stdDev, mean = Color.getStdDevAndMean('-dataset-fire_image')
    print "Stdev : "+str(stdDev), "Mean : "+str(mean)
    print "Video Frame : ",File.getCountFrame(videoFile)
    print "Video Size : ",len(File.readVideo(videoFile)[1]),len(File.readVideo(videoFile)[1][0])

    classifier = cls.getClassifier('-file-datatraining/TA.xls')
    fireFrame = numpy.array([0,0,0,0])
    list_wavelet = []
    list_color = Color.getFireArray('color_5x10^-9.txt')
    AllFrame = 0
    counter = 0

    starts = time.time()
    while(File.isOpened(videoFile)):
        try :
            #get curent frame
            currentFrame = File.readVideo(videoFile)[1]

            if len(currentFrame) == 0:
                return

            currentFrame2 = copy.copy(currentFrame)
            currentFrame = ImageProcessing.getDownSize(currentFrame)
            counter+=1

            # step 1 get moving pixel
            moving_time = time.time()
            movingFrame = Moving.getMovingForeGround(copy.copy(currentFrame))
            movingPixel = Moving.getMovingCandidatePixel(movingFrame)
            # moving = mv.getMovingForeGroundColor(currentFrame,movingFrame)

            # step 2 candidate pixel ( color probability )
            color_time = time.time()
            ColorCandidatePixel = Color.getColorCandidatePixel(copy.copy(movingPixel), copy.copy(currentFrame), list_color)

            #region growing
            region_time = time.time()
            region = RegionGrowing.getRegionGrowing(ColorCandidatePixel[0], copy.copy(currentFrame),list_color,counter)

            # step 3 region candidate pixel ( region size )
            size_time = time.time()
            sizeRegionCandidatePixel = RegionGrowing.getFilterSizeRegion(copy.copy(ColorCandidatePixel[0]),copy.copy(region))

            #preparing classification
            grayImage = ImageProcessing.getRGBtoGray(currentFrame2)
            LL,(HL,LH,HH) = wv.toWavelet(copy.copy(grayImage))

            list_wavelet.append([HL,LH,HH])
            if (counter<=10):
                continue
            list_wavelet.pop(0)

            classification_time = time.time()
            FinalCandidatePixel = cls.doClassification(classifier,copy.copy(sizeRegionCandidatePixel[0]),list_wavelet)

            final_time = time.time()
            fireFrameImage = (ImageProcessing.getUpSize(Moving.markingFire(FinalCandidatePixel[0],currentFrame2, 2)))
            fireFrameImage = ((Moving.markingFire(FinalCandidatePixel[0],currentFrame2, 2)))
            # print color_time-moving_time, region_time-color_time, size_time-region_time,classification_time-size_time,final_time-classification_time, (classification_time-moving_time)*30
            File.showVideo('Final',fireFrameImage)

            if len(movingPixel[0])>0:
                fireFrame[0]+=1
            if len(ColorCandidatePixel[0])>0:
                fireFrame[1]+=1
            if len(sizeRegionCandidatePixel[0])>0:
                fireFrame[2]+=1
            if len(FinalCandidatePixel[0])>0:
                fireFrame[3]+=1

            AllFrame+=1

            File.waitVideo(1)

        except :
            print "Time : ",time.time() - starts
            return (fireFrame)/float(AllFrame)
    print "Time : ",time.time() - starts
    return (fireFrame)/float(AllFrame)


if __name__ == '__main__':
    file = raw_input()

    path = '../../dataset/fix_data/'
    print file
    fileName = path+file

    File = preprocessing.File()
    videoFile = File.openVideo(fileName)
    res = readingVideo(videoFile)*100
    print "Acc : ",res,' %'
    report = []
    report.append(file)
    for y in res:
        report.append(y)
    # excel.writeAccuracy('-file-laporan/final_akurasi_5&5x10^-9.xls',report)

    print "Moving | Color | Size Region | Classififcation"
    File.closeVideo(videoFile)