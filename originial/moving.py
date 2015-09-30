__author__ = 'hamdiahmadi'
import data as dt
import cv2

#set learning rate
def setLearningRate(point):
    global learningRate
    learningRate = point

#get learning rate
def getLearningRate():
    global learningRate
    return learningRate

#get initial return initial
def getInit():
    global BckgrSbsMOG
    return BckgrSbsMOG

#get foreground moving image, return moving image 0 or 255
def getMovingForeGround(file):
    global BckgrSbsMOG
    return getInit().apply(file,learningRate = getLearningRate())

def getMovingForeGroundColor(original,file):
    file = dt.toBooleanImage(file)
    file = dt.to3Dimension(file)
    return original * file

#get moving pixel , return data as x and y ( coordinate )
def getMovingPixel(file):
    listPixel = dt.getMovingPixel(file)
    return listPixel

learningRate = 0.9
BckgrSbsMOG = cv2.BackgroundSubtractorMOG()

