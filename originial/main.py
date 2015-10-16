__author__ = 'hamdiahmadi'
import video as vd
import moving as mv
import pixelDetection as pd
import classification as cls
import wavelet as wv

def readingVideo(videoFile):
    stdDev, mean = pd.getStdDevAndMean('../../corped/__ChoosenImage2')
    print "Stdev : "+str(stdDev), "Mean : "+str(mean)
    print "Video Frame : ",vd.countFrame(videoFile)
    print "Video Size : ",len(vd.readVideo(videoFile)[1]),len(vd.readVideo(videoFile)[1][0])
    classifier = cls.getClassification()
    ListHighPassWavelet = wv.setData()
    counter = 0
    while(vd.isOpened(videoFile)):
        try :
            #get curent frame
            curentFrame = vd.readVideo(videoFile)[1]
            #get moving pixel
            movingFrame = mv.getMovingForeGround(vd.copyFile(curentFrame))
            movingPixel = mv.getMovingPixel(vd.copyFile(movingFrame))

            #get Candidate Pixel using Gaussian Distribution
            ListCandidatePixel = pd.getCandidatePixel(movingPixel, curentFrame, stdDev, mean)
            candidatePixel = mv.delPixel(ListCandidatePixel[1], mv.getMovingForeGroundColor(curentFrame,movingFrame))

            #wavelet
            LL,(HL,LH,HH) = wv.toWavelet(vd.toGray(curentFrame))
            ListHighPassWavelet[counter%10] = [LH,HL,HH]
            counter+=1
            if (counter < 10):
                continue
            ListFirePixel = cls.doClassification(classifier, ListCandidatePixel[0], ListHighPassWavelet)
            if len(ListCandidatePixel[0]) !=0 :
                print counter,len(ListFirePixel),len(ListCandidatePixel[0])

            vd.showVideo('original',curentFrame)
            vd.showVideo('haha',mv.getMovingForeGroundColor(curentFrame,movingFrame))
            vd.showVideo('haha2',candidatePixel)
            vd.waitVideo(1)
        except :
            print "Video Stopped"
            return
    return

if __name__ == '__main__':
    fileName = '../../dataset/data1/smoke_or_flame_like_object_3.avi'
    fileName = '../../dataset/Gundam Wing OP 2 HD.3gp'
    videoFile = vd.openVideo(fileName)
    res = readingVideo(videoFile)
    vd.closeVideo(videoFile)