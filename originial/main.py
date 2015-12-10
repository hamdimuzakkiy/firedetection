from preprocessing2 import luminance

__author__ = 'hamdiahmadi'
import video as vd
import moving as mv
import pixelDetection as pd
import classification as cls
import preprocessings as preprocessing
# import preprocessing as preprocessing
import wavelet as wv
import time
import copy
import numpy

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
    fireFrame = numpy.array([0,0,0,0,0,0,0])
    ListWavelet = []
    ListLuminance = []
    ListGrayImage = []
    ListRegion = []
    AllFrame = 0
    list_color = cdt.retriveColorList()
    starts = time.time()
    while(vd.isOpened(videoFile)):
        try :
            #get curent frame
            currentFrame = vd.readVideo(videoFile)[1]
            #compres image
            while (len(currentFrame)>150):
                if (len(currentFrame)<=300):
                    currentFrame2 = copy.copy(currentFrame)
                currentFrame = vd.downSize(currentFrame)
            counter+=1

            # step 1 get moving pixel
            movingFrame = mv.getMovingForeGround(vd.copyFile(currentFrame))
            movingPixel = mv.getMovingPixel(vd.copyFile(movingFrame))

            # step 2 candidate pixel ( color probability )
            # ColorCandidatePixel = cdt.getColorCandidatePixel(copy.copy(movingPixel), copy.copy(currentFrame), stdDev, mean)
            ColorCandidatePixel = cdt.getColorCandidatePixel2(copy.copy(movingPixel), copy.copy(currentFrame), list_color)

            #region growing
            # region = grw.getGrowingRegion(ColorCandidatePixel[0], copy.copy(currentFrame),stdDev, mean)
            region = grw.getGrowingRegion2(ColorCandidatePixel[0], copy.copy(currentFrame),list_color)

            # step 3 candidate pixel ( brightness ), convert image to gray with luminance and split by region
            luminanceImageGray = lum.getLuminanceImageGray(copy.copy(currentFrame))
            LuminanceCandidatePixel = idt.getLuminanceCandidatePixel(copy.copy(luminanceImageGray),copy.copy(ColorCandidatePixel[0]),copy.copy(region))

            # step 4 candidate pixel ( variance color per region ) -- issue on threshold --
            VarianceCandidatePixel = grw.getVarianceColorRegion(copy.copy(currentFrame),copy.copy(LuminanceCandidatePixel[0]),copy.copy(region))

            #preparing step 5 & 6
            grayImage = vd.toGray(currentFrame2)
            LL,(HL,LH,HH) = wv.toWavelet(copy.copy(grayImage))
            luminanceImage = lum.getLumiananceImage(currentFrame)

            ListLuminance.append(luminanceImage)
            ListWavelet.append([HL,LH,HH])
            ListGrayImage.append(copy.copy(grayImage))
            ListRegion.append(region)
            if (counter<=10):
                continue
            ListLuminance.pop(0)
            ListWavelet.pop(0)
            ListGrayImage.pop(0)
            ListRegion.pop(0)

            DiferenceCandidatePixel = idt.getDiferencePixel(ListLuminance,copy.copy(VarianceCandidatePixel[0]))

            RegionCenterMovement = grw.getGrowingCenterPoint(ListRegion,copy.copy(DiferenceCandidatePixel[0]))

            # DiferenceCandidatePixel = idt.getDiferencePixel2(ListLuminance,copy.copy(DiferenceCandidatePixel[0]))

            FinalCandidatePixel = cls.doClassification(classifier,copy.copy(RegionCenterMovement[0]),ListWavelet)
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

            fireFrameImage = vd.upSize(vd.upSize(mv.markPixelRectangle(FinalCandidatePixel[0],currentFrame)))
            vd.showVideo('Final',fireFrameImage)

            vd.waitVideo(1)

        except :
            print "Time : ",time.time() - starts
            return (fireFrame)/float(AllFrame)
    print "Time : ",time.time() - starts
    return (fireFrame)/float(AllFrame)


if __name__ == '__main__':
    fileName = '../../dataset/hasil/39.mp4'

    print fileName
    videoFile = vd.openVideo(fileName)
    res = readingVideo(videoFile)
    print "Acc : ",res*100,' %'
    print "Moving | Color | Luminance | Variance Color | Pixel Color Movement | Moving Center Point | Classififcation"
    vd.closeVideo(videoFile)