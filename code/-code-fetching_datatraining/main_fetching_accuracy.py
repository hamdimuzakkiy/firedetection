__author__ = 'hamdiahmadi'
import classification as cls

import excel
import preprocessing as preprocessing
import wavelet as wv
import time
import copy
import numpy
import classification

def readingVideo(videoFile,list_color):
    Color = preprocessing.ColorDetection()
    File = preprocessing.File()
    Intensity = preprocessing.Intensity()
    Luminance = preprocessing.Luminance()
    RegionGrowing = preprocessing.RegionGrowing()
    ImageProcessing = preprocessing.ImageProcessing()
    Moving = preprocessing.Moving()

    classifier = classification.getClassifier('../-file-datatraining/TA.xls')
    fireFrame = numpy.array([0,0,0,0,0,0,0])
    list_wavelet = []
    list_luminance = []
    list_gray_image = []
    list_region = []

    AllFrame = 0
    counter = 0

    while(File.isOpened(videoFile)):
        try :
            #get curent frame
            currentFrame = File.readVideo(videoFile)[1]
            #compres image
            while (len(currentFrame)>150):
                if (len(currentFrame)<=300):
                    currentFrame2 = copy.copy(currentFrame)
                currentFrame = ImageProcessing.getDownSize(currentFrame)
            counter+=1

            gray_image = ImageProcessing.getRGBtoGray(copy.copy(currentFrame))

            # step 1 get moving pixel
            movingFrame = Moving.getMovingForeGround(copy.copy(currentFrame))
            movingPixel = Moving.getMovingCandidatePixel(movingFrame)

            # step 2 candidate pixel ( color probability )
            ColorCandidatePixel = Color.getColorCandidatePixel(copy.copy(movingPixel), copy.copy(currentFrame), list_color)

            #region growing
            region = RegionGrowing.getRegionGrowing(ColorCandidatePixel[0], copy.copy(currentFrame),list_color,counter)

            # step 3 candidate pixel ( brightness ), convert image to gray with luminance and split by region
            luminanceImageGray = Luminance.getLuminanceImageGray(copy.copy(gray_image))
            LuminanceCandidatePixel = Intensity.getLuminanceCandidatePixel(copy.copy(luminanceImageGray),copy.copy(ColorCandidatePixel[0]),copy.copy(region))

            # step 4 candidate pixel ( variance color per region ) -- issue on threshold --
            VarianceCandidatePixel = RegionGrowing.getVarianceColorCandidatePixel(copy.copy(currentFrame),copy.copy(LuminanceCandidatePixel[0]),copy.copy(region))

            #preparing step 5 & 6
            grayImage = ImageProcessing.getRGBtoGray(currentFrame2)
            LL,(HL,LH,HH) = wv.toWavelet(copy.copy(grayImage))
            luminanceImage = Luminance.getLumiananceImage(copy.copy(gray_image))

            list_luminance.append(luminanceImage)
            list_wavelet.append([HL,LH,HH])
            list_gray_image.append(copy.copy(grayImage))
            list_region.append(region)
            if (counter<=10):
                continue
            list_luminance.pop(0)
            list_wavelet.pop(0)
            list_gray_image.pop(0)
            list_region.pop(0)

            DiferenceCandidatePixel = Intensity.getDifferenceCandidatePixel(list_luminance,copy.copy(VarianceCandidatePixel[0]))

            RegionCenterMovement = RegionGrowing.getMovingPointCandidatePixel2(list_region,copy.copy(DiferenceCandidatePixel[0]))

            FinalCandidatePixel = cls.doClassification(classifier,copy.copy(RegionCenterMovement[0]),list_wavelet)
            # FinalCandidatePixel = RegionCenterMovement

            fireFrameImage = (ImageProcessing.getUpSize(Moving.markingFire(FinalCandidatePixel[0],currentFrame2, 2)))
            File.showVideo('Final',fireFrameImage)

            if len(movingPixel[0])>0:
                fireFrame[0]+=1
            if len(ColorCandidatePixel[0])>0:
                fireFrame[1]+=1
            if len(LuminanceCandidatePixel[0])>0:
                fireFrame[2]+=1
            if len(VarianceCandidatePixel[0])>0:
                fireFrame[3]+=1
            if len(DiferenceCandidatePixel[0])>0:
                fireFrame[4]+=1
            if len(RegionCenterMovement[0])>0:
                fireFrame[5]+=1
            if len(FinalCandidatePixel[0])>0:
                fireFrame[6]+=1
            AllFrame+=1

            File.waitVideo(1)

        except :
            return (fireFrame)/float(AllFrame)
    return (fireFrame)/float(AllFrame)


if __name__ == '__main__':

    File = preprocessing.File()
    Color = preprocessing.ColorDetection()
    path = '../../../dataset/jalan'
    files = File.readFolder(path)
    list_color = Color.getFireArray('../color.txt')
    for x in files :
        fileName = path+'/'+x
        print fileName
        videoFile = File.openVideo(fileName)
        res = readingVideo(videoFile,list_color)
        res*=100
        report = []
        report.append(x)
        for y in res:
            report.append(y)
        excel.writeAccuracy('../-file-laporan/accurcy-non api.xls',report)
        print "Acc : ",res,' %'
        File.closeVideo(videoFile)