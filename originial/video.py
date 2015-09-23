__author__ = 'hamdiahmadi'
import cv2

#open video, path : 0 = camera, string = file
def openVideo(path):
    return cv2.VideoCapture(path)

def closeVideo(file):
    return file.release()

def isOpened(file):
    return file.isOpened()