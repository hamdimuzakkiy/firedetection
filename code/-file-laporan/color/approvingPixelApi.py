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

    list_color = Color.getFireArray('color.txt')
    counter = 0
    color_rgb = []
    while(File.isOpened(videoFile)):
        try :
            currentFrame = File.readVideo(videoFile)[1]
            while (len(currentFrame)>150):
                if (len(currentFrame)<=300):
                    currentFrame2 = copy.copy(currentFrame)
                currentFrame = ImageProcessing.getDownSize(currentFrame)
            counter+=1

            movingFrame = Moving.getMovingForeGround(copy.copy(currentFrame))
            movingPixel = Moving.getMovingCandidatePixel(movingFrame)

            for index in range(0,len(movingPixel[0])):
                y = movingPixel[0][index]
                x = movingPixel[1][index]
                b,g,r = currentFrame[y][x]
                color_rgb.append([b,g,r])

            ColorCandidatePixel = Color.getColorCandidatePixel(copy.copy(movingPixel), copy.copy(currentFrame), list_color)

            fireFrameImage = (ImageProcessing.getUpSize(Moving.markingFire(ColorCandidatePixel[0],currentFrame2, 2)))
            File.showVideo('Final',fireFrameImage)

            File.waitVideo(1)

        except :
            excel.writeColor('-file-laporan/color.xls',color_rgb)
            return
    return


if __name__ == '__main__':
    file = 'api_kayu1.avi'
    path = '../../dataset/fix_data/'
    print file
    fileName = path+file
    File = preprocessing.File()
    videoFile = File.openVideo(fileName)
    readingVideo(videoFile)
    File.closeVideo(videoFile)