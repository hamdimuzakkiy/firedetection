__author__ = 'hamdiahmadi'
import video as vd
import moving as mv
import pixelDetection as pd
import classification as cls
import wavelet as wv
import luminance as lu

def readingVideo(videoFile):
    stdDev, mean = pd.getStdDevAndMean('../../corped/__ChoosenImage2')
    print "Stdev : "+str(stdDev), "Mean : "+str(mean)
    print "Video Frame : ",vd.countFrame(videoFile)
    print "Video Size : ",len(vd.readVideo(videoFile)[1]),len(vd.readVideo(videoFile)[1][0])
    classifier = cls.getClassification()
    ListHighPassWavelet = wv.setData()
    ListMap = lu.setData()
    ListEdge = lu.setData()
    counter = 0
    sumLuminance = 0
    sumMoving = 0
    sumProb = 0
    sumFinal = 0
    sumFinal2 = 0
    sumFalsePixel = 0
    while(vd.isOpened(videoFile)):
        try :
            #get curent frame
            curentFrame = vd.readVideo(videoFile)[1]

            # get moving pixel
            movingFrame = mv.getMovingForeGround(vd.copyFile(curentFrame))
            movingPixel = mv.getMovingPixel(vd.copyFile(movingFrame))

            #get Candidate Pixel using Gaussian Distribution
            ListCandidatePixel = pd.getCandidatePixel(movingPixel, curentFrame, stdDev, mean)
            candidatePixel = mv.delPixel(ListCandidatePixel[1], mv.getMovingForeGroundColor(curentFrame,movingFrame))

            gaussian7 = vd.getGaussian(vd.toGray(curentFrame),7)
            gaussian13 = vd.getGaussian(vd.toGray(curentFrame),13)
            gaussian = (gaussian7+gaussian13)/2

            # vd.showVideo('newgauss',mv.delPixel2(vd.copyFile(gaussian7),threshold))
            vd.showVideo('newgauss',gaussian7)
            # edge = vd.getEdge(vd.toGray(curentFrame))

            # wavelet
            LL,(HL,LH,HH) = wv.toWavelet(vd.toGray(curentFrame))

            ListHighPassWavelet[counter%10] = [LH,HL,HH]
            # ListMap[counter%10] = gaussian
            # ListEdge[counter%10] = edge
            counter+=1
            if (counter < 10):
                continue


            # luminance = lu.getLuminancePixel(ListCandidatePixel[0], ListMap)

            luminancePixel,nonLuminance = lu.getLuminancePixel2(ListCandidatePixel[0],gaussian7)
            candidatePixel2 = mv.delPixel(nonLuminance, mv.getMovingForeGroundColor(candidatePixel,movingFrame))
            # print '-------------------',counter,"-------------------"
            # ListFirePixel = cls.doClassification(classifier, luminancePixel, ListHighPassWavelet)
            # ListFirePixel2 = cls.doClassification(classifier, ListCandidatePixel[0], ListHighPassWavelet)

            # sumFinal+=len(ListFirePixel)
            # sumFinal2+=len(ListFirePixel2)
            # sumLuminance+=len(luminancePixel)
            # sumMoving+=len(movingPixel[0])
            # sumProb+=len(ListCandidatePixel[0])

            # if (len(ListFirePixel)!=1010101):
            #     print counter,len(luminance),len(ListCandidatePixel[0]),len(ListFirePixel)

            # ListEdgePixel = lu.edge(ListFirePixel,ListEdge)
            # sumFalsePixel+=len(ListEdgePixel)
            # ListFirePixel = cls.doClassification(classifier, ListEdgePixel, ListHighPassWavelet)

            # if len(ListCandidatePixel[0]) !=0:
            #     print counter,len(ListFirePixel),len(luminance),len(ListCandidatePixel[0])

            vd.showVideo('original',curentFrame)
            vd.showVideo('Moving Detection',mv.getMovingForeGroundColor(curentFrame,movingFrame))
            vd.showVideo('Probability Detection',candidatePixel)
            vd.showVideo('Luminance',candidatePixel2)
            vd.waitVideo(1)
        except :
            print "Video Stopped : ", str(sumFalsePixel)
            print "Moving : ",sumMoving
            print "Probability : ",sumProb
            print "Luminance : ",sumLuminance
            print "Final : ",sumFinal
            print "Final2 : ",sumFinal2
            return
    return

if __name__ == '__main__':
    fileName = '../../dataset/data2/flame1.avi'
    fileName = '../../dataset/Ultimate Fail Compilation- Best Fire Fails.mp4'
    fileName = '../../dataset/Gundam Wing OP 2 HD.3gp'
    # fileName = 0
    print fileName
    videoFile = vd.openVideo(fileName)
    res = readingVideo(videoFile)
    vd.closeVideo(videoFile)