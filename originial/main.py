__author__ = 'hamdiahmadi'
import video as vd
import moving as mv


def readingVideo(videoFile):
    a=0
    while(vd.isOpened(videoFile)):

        curentFrame = vd.readVideo(videoFile)[1]
        movingFrame = mv.getMovingForeGround(curentFrame)
        movingPixel = mv.getMovingPixel(movingFrame)
        print movingPixel
        vd.waitVideo(1)
        a+=1
    return


if __name__ == '__main__':
    fileName = '../../dataset/Automatic Fire detection using CCD Camera.mp4'
    videoFile = vd.openVideo(fileName)
    readingVideo(videoFile)
    vd.closeVideo()

