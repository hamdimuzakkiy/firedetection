__author__ = 'hamdiahmadi'
import classification as cls

import preprocessing as preprocessing
import wavelet as wv
import time
import copy
import numpy
import moving as mv


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

    classifier = cls.getClassifier('-file-datatraining/TA.xls','rbf',5)
    fireFrame = numpy.array([0,0,0,0])
    list_wavelet = []
    list_color = Color.getFireArray('-dataset-fire_file/color_5x10^-9.txt')
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

            File.saveImage('-code-approving/'+str(counter)+'.png',currentFrame)
            File.saveImage('-code-approving/'+str(counter)+'_2.png',currentFrame2)

            # step 1 get moving pixel
            movingFrame = Moving.getMovingForeGround(copy.copy(currentFrame))
            movingPixel = Moving.getMovingCandidatePixel(movingFrame)
            mvng = mv.getMovingForeGroundColor(currentFrame,movingFrame)

            File.saveImage('-code-approving/mvng'+str(counter)+'.png',mvng)

            # step 2 candidate pixel ( color probability )
            ColorCandidatePixel = Color.getColorCandidatePixel(copy.copy(movingPixel), copy.copy(currentFrame), list_color)
            clr = mv.delPixel(ColorCandidatePixel[1], mvng)

            File.saveImage('-code-approving/clr'+str(counter)+'.png',clr)

            #region growing
            region = RegionGrowing.getRegionGrowing(ColorCandidatePixel[0], copy.copy(currentFrame),list_color,counter)

            reg = copy.copy(currentFrame)

            for y in range(0,len(region)):
                for x in range(0,len(region[y])):                    
                    if region[y][x] == 0:
                        reg[y][x] = [0,0,0]

            # step 3 region candidate pixel ( region size )
            sizeRegionCandidatePixel = RegionGrowing.getFilterSizeRegion(copy.copy(ColorCandidatePixel[0]),copy.copy(region))
            siz = mv.delPixel(sizeRegionCandidatePixel[1], clr)

            File.saveImage('-code-approving/siz'+str(counter)+'.png',siz)

            #preparing classification
            grayImage = ImageProcessing.getRGBtoGray(currentFrame2)
            LL,(HL,LH,HH) = wv.toWavelet(copy.copy(grayImage))

            list_wavelet.append([HL,LH,HH])
            if (counter<=10):
                continue
            list_wavelet.pop(0)

            FinalCandidatePixel = cls.doClassification(classifier,copy.copy(sizeRegionCandidatePixel[0]),list_wavelet)

            fireFrameImage = Moving.markingFire(FinalCandidatePixel[0],currentFrame2, 2)
            fre = mv.delPixel(FinalCandidatePixel[1], siz)
            File.saveImage('-code-approving/fre'+str(counter)+'.png',fre)

            # fireFrameImage = Moving.markingFire(FinalCandidatePixel[0],currentFrame)
            File.showVideo('Final',fireFrameImage)

            File.saveImage('-code-approving/fnl'+str(counter)+'.png',fireFrameImage)

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

    path = '../data uji/'
    print file
    fileName = path+file

    File = preprocessing.File()
    videoFile = File.openVideo(fileName)
    res = readingVideo(videoFile)*100
    print "Acc : ",res,' %'

    print "Moving | Color | Size Region | Classififcation"
    File.closeVideo(videoFile)