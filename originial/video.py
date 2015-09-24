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

#wait video
def waitVideo(sec):
    return cv2.waitKey(sec)