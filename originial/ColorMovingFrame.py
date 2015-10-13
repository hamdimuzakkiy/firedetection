__author__ = 'hamdiahmadi'
import video as vd
import moving as mv
import os

def readingVideo(videoFile):
    a=0
    global  videoName
    if os.path.exists('../../corpeds/'+videoName) == False :
        os.mkdir('../../corpeds/'+videoName)
    while(vd.isOpened(videoFile) and a != vd.countFrame(videoFile)-50):
        curentFrame = vd.readVideo(videoFile)[1]
        # movingFrame = mv.getMovingForeGround(curentFrame)
        # vd.saveFrame('../../corpeds/'+videoName+'/'+str(a)+'.png',mv.getMovingForeGroundColor(curentFrame,movingFrame))
        vd.saveFrame('../../corpeds/'+videoName+'/'+str(a)+'.png',curentFrame)
        vd.waitVideo(1)
        a+=1
    return

if __name__ == '__main__':
    listDir = os.listdir('../../dataset/data2')
    for i in listDir:
        videoName = i
        fileName = '../../dataset/data2/'+i
        videoFile = vd.openVideo(fileName)
        readingVideo(videoFile)
        vd.closeVideo(videoFile)
        break