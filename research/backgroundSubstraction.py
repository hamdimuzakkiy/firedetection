__author__ = 'hamdiahmadi'
import cv2
import numpy as np

def toGray(image):
    image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    return image

def init(image):
    global background
    global threshold
    background = toGray(image)
    print len(image)
    print len(image[0])
    threshold = [[0 for x in range(len(image[0]))] for x in range(len(image))]

def updateBackground(x,y,image):
    global background
    global alpha
    background[x][y] = float(alpha*background[x][y])+float(1-alpha)*float(image[x][y])

def updateThreshold(x,y,image):
    global background
    global threshold
    global alpha
    threshold[x][y] = float(alpha*threshold[x][y])+float(5*abs(image[x][y]-background[x][y]))

def getMoving(image,background):
    global threshold
    # res = image.copy()
    # for x in range(0, len(image)):
    #     for y in range(0, len(image[x])):
    #         res[x][y] = 255
            # if (np.uint8(abs(image[x][y]-background[x][y])) > threshold[x][y]):
            # if (res[x][y]>125):
            #     updateBackground(x,y,image)
            #     updateThreshold(x,y,image)
            #     res[x][y] = 255
            # else:
            #     res[x][y] = 0
    return 0
    return res

def getSubstraction(image):
    global background
    grayImage = toGray(image)

    movingImage = getMoving(grayImage,background)
    cv2.imshow("new",grayImage)



    # if (background != grayImage).any():
    #     pass
    # else:
    #     print"same"

    background = grayImage
    return background

background = ''
threshold = ''
alpha = 0.7