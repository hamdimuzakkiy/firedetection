from preprocessing2 import luminance

__author__ = 'hamdiahmadi'
import video as vd
import moving as mv
import pixelDetection as pd
import classification as cls
import preprocessing
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
    grw = preprocessing.growing()

    classifier = ''
    ListWavelet = []
    ListLuminance = []
    ListGrayImage = []
    cntr = 0
    while(vd.isOpened(videoFile)):
        try :
            currentFrame = vd.readVideo(videoFile)[1]
            while (len(currentFrame)>150):
                if (len(currentFrame)<=300):
                    currentFrame2 = copy.copy(currentFrame)
                currentFrame = vd.downSize(currentFrame)
            movingFrame = mv.getMovingForeGround(vd.copyFile(currentFrame))
            movingPixel = mv.getMovingPixel(vd.copyFile(movingFrame))
            ColorCandidatePixel = cdt.getColorCandidatePixel(copy.copy(movingPixel), copy.copy(currentFrame), stdDev, mean)
            region = grw.getGrowingRegion(ColorCandidatePixel[0], copy.copy(currentFrame),stdDev, mean)
            luminanceImageGray = lum.getLuminanceImageGray(copy.copy(currentFrame))
            LuminanceCandidatePixel = idt.getLuminanceCandidatePixel(copy.copy(luminanceImageGray),copy.copy(ColorCandidatePixel[0]),copy.copy(region))
            VarianceCandidatePixel = grw.getVarianceColorRegion(copy.copy(currentFrame),copy.copy(LuminanceCandidatePixel[0]),copy.copy(region))
            grayImage = vd.toGray(currentFrame2)
            LL,(HL,LH,HH) = wv.toWavelet(copy.copy(grayImage))
            luminanceImage = lum.getLumiananceImage(currentFrame)
            ListLuminance.append(luminanceImage)

            # vd.saveFrame('temporary/LH.png',LH)
            # vd.saveFrame('temporary/HL.png',HL)
            # vd.saveFrame('temporary/HH.png',HH)
            #
            # LH = vd.readImage('temporary/LH.png')
            # HL = vd.readImage('temporary/HL.png')
            # HH = vd.readImage('temporary/HH.png')
            #
            # LH = LH[:,:,2]
            # HL = HL[:,:,2]
            # HH = HH[:,:,2]

            ListWavelet.append([HL,LH,HH])


            ListGrayImage.append(copy.copy(grayImage))
            counter+=1
            if (counter<=10):
                continue

            ListLuminance.pop(0)
            ListWavelet.pop(0)
            ListGrayImage.pop(0)
            DiferenceCandidatePixel = idt.getDiferencePixel(ListLuminance,copy.copy(VarianceCandidatePixel[0]))
            data = cls.returnDataTraining(classifier,DiferenceCandidatePixel[0],ListWavelet,classes)
            fireFrameImage = vd.upSize(vd.upSize(mv.markPixelRectangle(DiferenceCandidatePixel[0],currentFrame)))
            vd.showVideo('Final',fireFrameImage)
            vd.waitVideo(1)
            for x in data:
                # if cntr == 673:
                #     return
                cntr+=1
                excel.saveDataSet('TA.xls',x,classes)
        except ValueError:
            print ValueError
            return
    return


if __name__ == '__main__':
    fileName = '../../../dataset/data2/flame2.avi'
    fileName = '../../../dataset/uji/Red Velvet - Dumb Dumb Dance Compilation [Mirrored].mp4'
    # fileName = '../../../dataset/data3/IMG_7358.MOV'
    # fileName = '../../../dataset/data1/smoke_or_flame_like_object_1.avi'
    fileName = '../../../dataset/Armed gangs fight in the middle of a busy road in China.mp4'
    # fileName = 0

    print fileName
    videoFile = vd.openVideo(fileName)
    start = time.time()
    classes =  'Bukan Api'
    res = readingVideo(videoFile,classes)
    print time.time() - start
    vd.closeVideo(videoFile)