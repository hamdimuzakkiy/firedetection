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
    Intensity = preprocessing.Intensity()
    Luminance = preprocessing.Luminance()
    RegionGrowing = preprocessing.RegionGrowing()
    ImageProcessing = preprocessing.ImageProcessing()
    Moving = preprocessing.Moving()

    stdDev, mean = Color.getStdDevAndMean('-dataset-fire_image')
    print "Stdev : "+str(stdDev), "Mean : "+str(mean)
    print "Video Frame : ",File.getCountFrame(videoFile)
    print "Video Size : ",len(File.readVideo(videoFile)[1]),len(File.readVideo(videoFile)[1][0])

    classifier = cls.getClassifier('-file-datatraining/TA.xls')
    fireFrame = numpy.array([0,0,0,0,0,0,0])
    list_wavelet = []
    list_luminance = []
    list_gray_image = []
    list_region = []
    list_color = Color.getFireArray('color.txt')
    AllFrame = 0
    counter = 0

    starts = time.time()
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
            # moving = mv.getMovingForeGroundColor(currentFrame,movingFrame)
            # File.saveImage('tmp/'+str(counter)+'_.png',moving)
            # File.saveImage('tmp/'+str(counter)+'.png',currentFrame)

            # step 2 candidate pixel ( color probability )
            ColorCandidatePixel = Color.getColorCandidatePixel(copy.copy(movingPixel), copy.copy(currentFrame), list_color)

            #region growing
            region = RegionGrowing.getRegionGrowing(ColorCandidatePixel[0], copy.copy(currentFrame),list_color,counter)

            # step 3 candidate pixel ( brightness ), convert image to gray with luminance and split by region
            LuminanceCandidatePixel = ColorCandidatePixel

            VarianceCandidatePixel = RegionGrowing.getVarianceColorCandidatePixel(copy.copy(currentFrame),copy.copy(LuminanceCandidatePixel[0]),copy.copy(region))

            fireFrameImage = (ImageProcessing.getUpSize(Moving.markingFire(VarianceCandidatePixel[0],currentFrame2, 2)))
            File.showVideo('Final',fireFrameImage)

            File.waitVideo(1)
        except :
            return


if __name__ == '__main__':
    file = 'non_api_hamdi1.avi'
    path = '../../dataset/fix_data/'
    print file
    fileName = path+file
    File = preprocessing.File()
    videoFile = File.openVideo(fileName)
    readingVideo(videoFile)
    File.closeVideo(videoFile)