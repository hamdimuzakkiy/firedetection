__author__ = 'hamdiahmadi'
import classification as cls

import preprocessing as preprocessing
import wavelet as wv
import copy
import classification
import excel

def readingVideo(videoFile, list_color, classes):
    Color = preprocessing.ColorDetection()
    File = preprocessing.File()
    Intensity = preprocessing.Intensity()
    Luminance = preprocessing.Luminance()
    RegionGrowing = preprocessing.RegionGrowing()
    ImageProcessing = preprocessing.ImageProcessing()
    Moving = preprocessing.Moving()

    list_wavelet = []
    list_luminance = []
    list_gray_image = []
    list_region = []
    counter = 0

    feature = []
    feature.append(['-','-','-','-','-','-','-','-','-','-'])
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

            tmp_feature = classification.returnDataTraining(RegionCenterMovement[0],list_wavelet)
            feature.append(tmp_feature)
            fireFrameImage = (ImageProcessing.getUpSize(Moving.markingFire(RegionCenterMovement[0],currentFrame2, 2)))
            File.showVideo('result',fireFrameImage)
            File.waitVideo(1)

        except:
            excel.writeDataTraining('../-file-datatraining/api_TA2.xls',feature,classes)
            return
    return

def getFolder(folder,classes):
    File = preprocessing.File()
    Color = preprocessing.ColorDetection()
    path = folder
    files = File.readFolder(path)
    list_color = Color.getFireArray('../color.txt')
    for x in files :
        fileName = path+'/'+x
        print fileName
        videoFile = File.openVideo(fileName)
        readingVideo(videoFile,list_color,classes)
        File.closeVideo(videoFile)

def getFile(file,classes):
    fileName = file
    print fileName
    Color = preprocessing.ColorDetection()
    list_color = Color.getFireArray('../color.txt')
    File = preprocessing.File()
    videoFile = File.openVideo(fileName)
    readingVideo(videoFile,list_color,classes)
    File.closeVideo(videoFile)

if __name__ == '__main__':
    # getFolder('../../../dataset/datatraining/non api','Bukan Api')
    getFile('../../../dataset/fix_data/api_mobil3.avi','Api')