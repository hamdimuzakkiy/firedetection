__author__ = 'hamdiahmadi'

import numpy as np
import cv2
import backgroundSubstraction as bg


nameFile = 'Automatic Fire detection using CCD Camera.mp4'
# nameFile = 0
# doc : requirment : copy opencv_ffmpeg.dll from opencv to python27 folder
O_capture = cv2.VideoCapture(nameFile) #param = "file name" or "device", 0 as device ( local cam )
print "Status : ",O_capture.isOpened()

frameCount = O_capture.get(7)
a=0
# while (O_capture.isOpened()):
#     image = O_capture.read()[1]
#     a+=1
#     if (a == frameCount-1):
#         break
#     if (a==1):
#         bg.init(image)
#         continue
#     substractImage = bg.getSubstraction(image)
#     cv2.waitKey(1)

substract = cv2.BackgroundSubtractorMOG()

while (O_capture.isOpened()):

    ret, img = O_capture.read()
    substract2 = substract.apply(img,learningRate = 0.9)

    cv2.imshow("test2",substract2)
    cv2.imshow("origin",img)
    k = cv2.waitKey(1)
    if (a == frameCount-1):
        break
    a+=1



O_capture.release()
cv2.destroyAllWindows()