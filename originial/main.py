__author__ = 'hamdiahmadi'
import video as vd
import moving as mv
import pixelDetection as pd


def readingVideo(videoFile):
    stdDev, mean = pd.getStdDevAndMean('../../corped/__ChoosenImage2')
    print "Stdev : "+str(stdDev), "Mean : "+str(mean)
    print vd.countFrame(videoFile)
    while(vd.isOpened(videoFile)):
        curentFrame = vd.readVideo(videoFile)[1]
        movingFrame = mv.getMovingForeGround(vd.copyFile(curentFrame))
        movingPixel = mv.getMovingPixel(vd.copyFile(movingFrame))
        ListCandidatePixel = pd.getCandidatePixel(movingPixel, curentFrame, stdDev, mean)
        # candidatePixel = mv.delPixel(ListCandidatePixel[1], mv.getMovingForeGroundColor(curentFrame,movingFrame))

        # print len(ListCandidatePixel[1])
        # for x in range(0,len(ListCandidatePixel[1])):
        #     print mv.getMovingForeGroundColor(curentFrame,movingFrame)[ListCandidatePixel[1][x][0]][ListCandidatePixel[1][x][1]]
            # print mv.getMovingForeGroundColor(curentFrame,movingFrame)[candidatePixel[x][0]][candidatePixel[x][1]]
        vd.showVideo('original',curentFrame)
        vd.showVideo('haha',mv.getMovingForeGroundColor(curentFrame,movingFrame))
        # vd.showVideo('haha2',candidatePixel)
        vd.waitVideo(1)

    return

if __name__ == '__main__':
    # fileName = '../../dataset/data1/smoke_or_flame_like_object_1.avi'
    fileName = '../../dataset/Automatic Fire detection using CCD Camera.mp4'
    fileName = 0
    videoFile = vd.openVideo(fileName)
    readingVideo(videoFile)
    vd.closeVideo(videoFile)