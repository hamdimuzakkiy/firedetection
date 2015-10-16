__author__ = 'hamdiahmadi'
import video as vd
import moving as mv
import pixelDetection as pd
import numpy

def readingVideo(videoFile):
    stdDev, mean = pd.getStdDevAndMean('../../corped/__ChoosenImage2')
    print "Stdev : "+str(stdDev), "Mean : "+str(mean)
    print "Video Frame : ",vd.countFrame(videoFile)
    print "Video Size : ",len(vd.readVideo(videoFile)[1]),len(vd.readVideo(videoFile)[1][0])

    count = 0
    # arr = [[[0,x,y] for x in range(len(vd.readVideo(videoFile)[1][0]))] for y in range(len(vd.readVideo(videoFile)[1]))]
    # arr2 = dict()
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
            vd.showVideo('haha2',candidatePixel)
            print count,ListCandidatePixel[0]
            # for x in ListCandidatePixel[0]:
                # arr[x[0]][x[1]][0]+=1
            if (count == 100):
                pass
                # return arr
            count+=1
            vd.waitVideo(1)
        except :
            print "Video Stopped"
            return
    return

if __name__ == '__main__':
    fileName = '../../dataset/data1/smoke_or_flame_like_object_2.avi'
    videoFile = vd.openVideo(fileName)
    res = readingVideo(videoFile)
    vd.closeVideo(videoFile)