__author__ = 'hamdiahmadi'
import video as vd
import moving as mv
import pixelDetection as pd

def readingVideo(videoFile):
    stdDev, mean = pd.getStdDevAndMean('../../corped/__ChoosenImage2')
    print "Stdev : "+str(stdDev), "Mean : "+str(mean)
    print "Video Frame : ",vd.countFrame(videoFile)
    print "Video Size : ",len(vd.readVideo(videoFile)[1]),len(vd.readVideo(videoFile)[1][0])
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

            vd.showVideo('original',curentFrame)
            vd.showVideo('haha',mv.getMovingForeGroundColor(curentFrame,movingFrame))
            vd.showVideo('haha2',candidatePixel)
            vd.waitVideo(1)

        except :
            print "Video Stopped"
            return
    return

if __name__ == '__main__':
    fileName = '../../dataset/data1/smoke_or_flame_like_object_1.avi'
    videoFile = vd.openVideo(fileName)
    readingVideo(videoFile)
    vd.closeVideo(videoFile)