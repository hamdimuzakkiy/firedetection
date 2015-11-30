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
import excel

user_input = [None]

def get_user_input(user_input_ref):
    user_input_ref[0] = raw_input("Give me some Information: ")

def readingVideo(videoFile,classes):
    stdDev, mean = pd.getStdDevAndMean('../__ChoosenImage2')

    counter = 0
    cdt = preprocessing.colorDetection()
    idt = preprocessing.intensityDetection()
    lum = preprocessing.luminance()

    classifier = ''
    ListWavelet = []
    ListLuminance = []
    ListGrayImage = []

    while(vd.isOpened(videoFile)):
        try :
            currentFrame = vd.readVideo(videoFile)[1]
            while (len(currentFrame)>150):
                if (len(currentFrame)<=300):
                    currentFrame2 = copy.copy(currentFrame)
                currentFrame = vd.downSize(currentFrame)
            movingFrame = mv.getMovingForeGround(vd.copyFile(currentFrame))
            movingPixel = mv.getMovingPixel(vd.copyFile(movingFrame))
            ColorCandidatePixel = cdt.getCandidatePixel(copy.copy(movingPixel), currentFrame, stdDev, mean)
            luminanceImageGray = lum.getLuminanceImageGray(currentFrame)
            LuminanceCandidatePixel = idt.getIntensityPixel(luminanceImageGray,copy.copy(ColorCandidatePixel[0]),copy.copy(movingPixel))
            grayImage = vd.toGray(currentFrame2)
            LL,(HL,LH,HH) = wv.toWavelet(copy.copy(grayImage))
            luminanceImage = lum.getLumiananceImage(currentFrame)
            ListLuminance.append(luminanceImage)
            ListWavelet.append([HL,LH,HH])
            ListGrayImage.append(copy.copy(grayImage))
            counter+=1
            if (counter<=10):
                continue
            ListLuminance.pop(0)
            ListWavelet.pop(0)
            ListGrayImage.pop(0)

            ListCandidatePixel = idt.getDiferencePixel(ListLuminance,copy.copy(LuminanceCandidatePixel[0]))
            data = cls.returnDataTraining(classifier,ListCandidatePixel[0],ListWavelet,classes)
            fireFrameImage = vd.upSize(vd.upSize(mv.markPixelRectangle(ListCandidatePixel[0],currentFrame)))
            vd.showVideo('Final',fireFrameImage)
            for x in data:
                excel.saveDataSet('TA.xls',x,classes)

            vd.waitVideo(1)
        except :
            return
    return


if __name__ == '__main__':
    fileName = '../../../dataset/data2/flame1.avi'
    # fileName = '../../dataset/uji/Man on Fire Building Jump - 9 Story Drop of Doom.mp4'
    # fileName = '../../dataset/data3/IMG_7358.MOV'
    # fileName = '../../dataset/data1/smoke_or_flame_like_object_2.avi'
    # fileName = '../../dataset/Automatic Fire detection using CCD Camera.mp4'
    fileName = 0

    print fileName
    videoFile = vd.openVideo(fileName)
    start = time.time()
    classes = 'Bukan Api'
    res = readingVideo(videoFile,classes)
    print time.time() - start
    vd.closeVideo(videoFile)