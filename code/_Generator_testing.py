__author__ = 'hamdiahmadi'
import classification as cls

import excel
import preprocessing as preprocessing
import wavelet as wv
import time
import copy
import numpy


def readingVideo(videoFile,list_color,classifier,file_name):
    Color = preprocessing.ColorDetection()
    File = preprocessing.File()
    RegionGrowing = preprocessing.RegionGrowing()
    ImageProcessing = preprocessing.ImageProcessing()
    Moving = preprocessing.Moving()
    
    fireFrame = numpy.array([0,0,0,0])
    list_wavelet = []
    AllFrame = 0
    counter = 0

    starts = time.time()
    while(File.isOpened(videoFile)):
        try :
            currentFrame = File.readVideo(videoFile)[1]
            if len(currentFrame) == 0:
                return
            currentFrame2 = copy.copy(currentFrame)
            currentFrame = ImageProcessing.getDownSize(currentFrame)
            counter+=1
            movingFrame = Moving.getMovingForeGround(copy.copy(currentFrame))
            movingPixel = Moving.getMovingCandidatePixel(movingFrame)
            ColorCandidatePixel = Color.getColorCandidatePixel(copy.copy(movingPixel), copy.copy(currentFrame), list_color)
            region = RegionGrowing.getRegionGrowing(ColorCandidatePixel[0], copy.copy(currentFrame),list_color,counter)
            sizeRegionCandidatePixel = RegionGrowing.getFilterSizeRegion(copy.copy(ColorCandidatePixel[0]),copy.copy(region))
            grayImage = ImageProcessing.getRGBtoGray(currentFrame2)
            LL,(HL,LH,HH) = wv.toWavelet(copy.copy(grayImage))
            list_wavelet.append([HL,LH,HH])
            if (counter<=10):
                continue
            list_wavelet.pop(0)
            FinalCandidatePixel = cls.doClassification(classifier,copy.copy(sizeRegionCandidatePixel[0]),list_wavelet)
            fireFrameImage = ImageProcessing.getUpSize((Moving.markingFire(FinalCandidatePixel[0],currentFrame2, 2)))
            File.showVideo('Final',fireFrameImage)
            File.saveImage('-laporan- gambar/'+file_name+str(counter)+'.png',fireFrameImage)
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
            return (fireFrame)/float(AllFrame),File.getCountFrame(videoFile),time.time() - starts
    print "Time : ",time.time() - starts
    return (fireFrame)/float(AllFrame),File.getCountFrame(videoFile),time.time() - starts


if __name__ == '__main__':
    list_variance = []
    # list_variance.append(['color_10^-7.txt',5,'rbf','10^-7_5_rbf.xls'])
    # list_variance.append(['color_10^-8.txt',5,'rbf','10^-8_5_rbf.xls'])
    # list_variance.append(['color_5x10^-9.txt',5,'rbf','5x10^-9_5_rbf3.xls'])
    # list_variance.append(['color_10^-9.txt',5,'rbf','10^-9_5_rbf.xls'])
    #
    # list_variance.append(['color_5x10^-9.txt',1,'rbf','5x10^-9_1_rbf.xls'])
    # list_variance.append(['color_5x10^-9.txt',3.5,'rbf','5x10^-9_3.5_rbf.xls'])
    list_variance.append(['-dataset-fire_file/color_5x10^-9.txt',7,'rbf','5x10^-9_7_rbf.xls'])
    #
    # list_variance.append(['color_5x10^-9.txt',5,'poly','5x10^-9_5_poly.xls'])
    # list_variance.append(['color_5x10^-9.txt',5,'poly','5x10^-9_5_linear.xls'])
    for variasi in list_variance:
        print variasi
        path = '../data uji/'
        File = preprocessing.File()
        Color = preprocessing.ColorDetection()
        list_file = File.readFolder(path)
        classifier = cls.getClassifier('-file-datatraining/TA.xls',variasi[2],variasi[1])
        list_color = Color.getFireArray(variasi[0])
        for x in list_file:
            preprocessing = reload(preprocessing)
            print x
            fileName = path+x
            videoFile = File.openVideo(fileName)
            res, frameCounter, times = readingVideo(videoFile,list_color,classifier,x)
            res*=100
            print "Acc : ",res,' %'
            report = []
            report.append(x)
            for y in res:
                report.append(y)
            report.append('')
            report.append(frameCounter)
            report.append(times)
            # excel.writeAccuracy('-file-laporan/'+variasi[3],report)
            print "Moving | Color | Size Region | Classififcation"
            File.closeVideo(videoFile)