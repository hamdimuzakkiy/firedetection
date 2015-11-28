__author__ = 'hamdiahmadi'
import video as vd
import moving as mv
import pixelDetection as pd
import classification as cls
import preprocessing2 as preprocessing
import wavelet as wv
import time
import copy
import cv2

def readingVideo(videoFile):
    stdDev, mean = pd.getStdDevAndMean('../../corped/__ChoosenImage2')
    print "Stdev : "+str(stdDev), "Mean : "+str(mean)
    print "Video Frame : ",vd.countFrame(videoFile)
    print "Video Size : ",len(vd.readVideo(videoFile)[1]),len(vd.readVideo(videoFile)[1][0])
    counter = 0

    pdt = preprocessing.pixelDetection()
    idt = preprocessing.intensityDetection()
    lum = preprocessing.luminance()
    classifier = cls.getClassification()
    ListWavelet = []
    ListMap = []
    ListOriginal = []
    ListLuminance = []
    while(vd.isOpened(videoFile)):
        try :
            #get curent frame
            currentFrame = vd.readVideo(videoFile)[1]

            #compres image
            while (len(currentFrame)>150):
                if (len(currentFrame)<=300):
                    currentFrame2 = copy.copy(currentFrame)
                currentFrame = vd.downSize(currentFrame)

            # get moving pixel
            movingFrame = mv.getMovingForeGround(vd.copyFile(currentFrame))
            movingPixel = mv.getMovingPixel(vd.copyFile(movingFrame))

            #candidate pixel ( color probability )
            ListCandidatePixel = pdt.getCandidatePixel(movingPixel, currentFrame, stdDev, mean)
            candidatePixel = mv.delPixel(ListCandidatePixel[1], mv.getMovingForeGroundColor(currentFrame,movingFrame))


            gray = vd.toGray(currentFrame)
            gaussian13 = vd.getGaussian(gray,13)
            gaussian7 = vd.getGaussian(gray,7)
            gaussians = cv2.add((gaussian7/2),(gaussian13/2))

            vd.showVideo("Gaussian",((gaussians)))

            #wavelet
            LL,(HL,LH,HH) = wv.toWavelet(vd.getGaussian(vd.toGray(currentFrame2),7))
            # LL,(HL,LH,HH) = wv.toWavelet(currentFrame2[:,:,2])

            ListWavelet.append([LH,HL,HH])
            ListMap.append(gray)
            ListOriginal.append(currentFrame)
            ListLuminance.append(gaussians)
            counter+=1
            if (counter <= 10):
                continue

            ListWavelet.pop(0)
            ListMap.pop(0)
            ListOriginal.pop(0)
            ListLuminance.pop(0)

            # lum.luminanceRemoval(ListLuminance,ListCandidatePixel[0])


            # > deviasi
            ListCandidatePixel1 = idt.getCandidatePixel(gaussian13,ListCandidatePixel[0])
            candidatePixel1 = mv.delPixel(ListCandidatePixel1[1], copy.copy(candidatePixel))

            # vd.showVideo("Candidate 1",(cv2.pyrUp(candidatePixel1)))

            ListCandidatePixel2 = ListCandidatePixel1
            #candidate pixel based on x,y pixel with 10 frame
            ListCandidatePixel3 = idt.getCandidatePixel3(ListMap,ListCandidatePixel2[0])
            candidatePixel3 = mv.delPixel(ListCandidatePixel3[1],mv.delPixel(ListCandidatePixel2[1], copy.copy(candidatePixel1)))

            # vd.showVideo("Candidate Pixel 3",(vd.upSize(candidatePixel3)))

            ListCandidatePixel5 = idt.getCandidatePixel5(ListOriginal,ListCandidatePixel3[0],stdDev,mean)
            candidatePixel5 = mv.delPixel(ListCandidatePixel5[1],candidatePixel3)

            # vd.showVideo("Candidate Pixel 5",(vd.upSize(candidatePixel5)))
            ListFirePixel = cls.doClassification(classifier, ListCandidatePixel5[0], ListWavelet)
            candidatePixel4 = mv.delPixel(ListFirePixel[1],candidatePixel3)
            finalPixel3 = mv.markPixel(ListFirePixel[0],currentFrame)

            vd.showVideo("Final Candidate Black",((candidatePixel4)))
            vd.showVideo("Final Candidate",vd.upSize(vd.upSize(finalPixel3)))

            # print len(ListCandidatePixel1[0]),len(ListCandidatePixel3[0]),len(ListFirePixel[0])

            vd.waitVideo(1)
        except:
            return
    return

if __name__ == '__main__':
    fileName = '../../dataset/data2/flame1.avi'
    # fileName = '../../dataset/uji/forest2.avi'
    # fileName = '../../dataset/data3/IMG_7358.MOV'
    fileName = '../../dataset/data1/smoke_or_flame_like_object_1.avi'
    # fileName = '../../dataset/Automatic Fire detection using CCD Camera.mp4'
    # fileName = 0

    print fileName
    videoFile = vd.openVideo(fileName)
    start = time.time()
    res = readingVideo(videoFile)
    print time.time() - start
    vd.closeVideo(videoFile)