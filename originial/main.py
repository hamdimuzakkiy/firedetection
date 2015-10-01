__author__ = 'hamdiahmadi'
import video as vd
import moving as mv
import  pixelDetection as pd

def readingVideo(videoFile):
    stdDev, mean = pd.getStdDevAndMean('../../corped/__ChoosenImage2')
    print "Stdev : "+str(stdDev), "Mean : "+str(mean)
    while(vd.isOpened(videoFile)):

        curentFrame = vd.readVideo(videoFile)[1]
        movingFrame = mv.getMovingForeGround(vd.copyFile(curentFrame))
        movingPixel = mv.getMovingPixel(vd.copyFile(movingFrame))
        candidatePixel = pd.getCandidatePixel(movingPixel, curentFrame, stdDev, mean)
        foregroundImage = mv.getMovingForeGroundColor(vd.copyFile(curentFrame),vd.copyFile(movingFrame))
        # movingFrame2 =
        # vd.showVideo('haha',mv.getMovingForeGroundColor(curentFrame,movingFrame))
        vd.showVideo('haha',curentFrame)
        vd.waitVideo(1)

    return

if __name__ == '__main__':
    fileName = '../../dataset/data2/flame1.avi'
    videoFile = vd.openVideo(fileName)
    readingVideo(videoFile)
    vd.closeVideo(videoFile)