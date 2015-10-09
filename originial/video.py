__author__ = 'hamdiahmadi'
import cv2

#open video, path : 0 = camera, string = file | return init to read video
def openVideo(path):
    return cv2.VideoCapture(path)

#close video if finish | return release video
def closeVideo(file):
    return file.release()

#return boolean to check the video oppened or not
def isOpened(file):
    return file.isOpened()

#show image , return to show imshow
def showVideo(name,image):
    return cv2.imshow(name,image)

#reading video, return 2 param : status, image
def readVideo(file):
    return file.read()

def saveFrame(name,image):
    return cv2.imwrite(name,image)

def readImage(file):
    return cv2.imread(file)
#wait video
def waitVideo(sec):
    return cv2.waitKey(sec)

def countFrame(file):
    return file.get(7)

def copyFile(file):
    return file.copy()

def toGray(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)