__author__ = 'hamdiahmadi'
import video as vd
import moving as mv
import pixelDetection as pd
import preprocessing3 as preprocessing
import time


def readingVideo(videoFile):
    stdDev, mean = pd.getStdDevAndMean('../../corped/__ChoosenImage2')
    print "Stdev : "+str(stdDev), "Mean : "+str(mean)
    print "Video Frame : ",vd.countFrame(videoFile)
    print "Video Size : ",len(vd.readVideo(videoFile)[1]),len(vd.readVideo(videoFile)[1][0])
    counter = 0

    pdt = preprocessing.pixelDetection()
    idt = preprocessing.intensityDetection()

    while(vd.isOpened(videoFile)):
        try :
            #get curent frame
            currentFrame = vd.readVideo(videoFile)[1]

            # get moving pixel
            movingFrame = mv.getMovingForeGround(vd.copyFile(currentFrame))
            movingPixel = mv.getMovingPixel(vd.copyFile(movingFrame))

            start1 = time.time()
            ListCandidatePixel = pdt.getCandidatePixel(movingPixel, currentFrame, stdDev, mean)
            candidatePixel = mv.delPixel(ListCandidatePixel[1], mv.getMovingForeGroundColor(currentFrame,movingFrame))
            end1 = time.time()

            start = time.time()
            gaussian7 = vd.getGaussian(vd.toGray(currentFrame),7)
            ListCandidatePixel2 = idt.getCandidatePixel(gaussian7,ListCandidatePixel[0])
            candidatePixel2 = mv.delPixel(ListCandidatePixel2[1], candidatePixel)
            print len(ListCandidatePixel[0]),len(ListCandidatePixel2[0]),end1-start1,time.time()-start

            vd.showVideo("Real",currentFrame)
            vd.showVideo("Probability",candidatePixel)
            vd.showVideo("Intensity",candidatePixel2)
            counter+=1
            if (counter < 10):
                continue

            vd.waitVideo(1)
        except :

            return
    return

if __name__ == '__main__':
    fileName = '../../dataset/data1/smoke_or_flame_like_object_1.avi'
    fileName = '../../dataset/Automatic Fire detection using CCD Camera.mp4'
    # fileName = 0
    print fileName
    videoFile = vd.openVideo(fileName)
    res = readingVideo(videoFile)
    vd.closeVideo(videoFile)