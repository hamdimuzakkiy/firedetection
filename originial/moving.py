__author__ = 'hamdiahmadi'
import data as dt
import cv2
import copy
import numpy as np

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

# making list pixel to black
def delPixel(list, image):
    for x in range(0,len(list)):
        image [list[x][0]][list[x][1]] = [0,0,0]
    return image

def delPixel2(image, threshold):
    for y in range(0,len(image)):
        for x in range(0,len(image[y])):
            if image[y][x] < threshold:
                image[y][x] = 0
    return image

def clock():
    clocks = []
    clocks.append([-1,-1])
    clocks.append([-1,0])
    clocks.append([-1,1])
    clocks.append([0,-1])
    clocks.append([0,1])
    clocks.append([1,-1])
    clocks.append([1,0])
    clocks.append([1,1])
    return clocks

def markPixel(list,image):
    res = copy.copy(image)
    clocks = clock()
    for x in list:
        coor_x = x[1]
        coor_y = x[0]
        for y in clocks:
            if coor_y + y[0] < 0 or coor_y + y[0] > len(image)-1 or coor_x + y[1] < 0 or coor_x + y[1] > len(image[0])-1:
                continue
            res[coor_y][coor_x] = [255,191,0]
    return res

def markPixelBnW(list,image):
    res = copy.copy(image)
    clocks = clock()
    for x in list:
        res[x[0]][x[1]]= 0
    return res

def markPixelRectangle(list,image):
    if len(list) == 0:
        return image
    list = np.array(list)

    minY,maxY =  min(list[:,0]),max(list[:,0])
    minX,maxX =  min(list[:,1]),max(list[:,1])

    for y in range(minY,maxY+1):
        image[y][minX] = [255,191,0]
        image[y][maxX] = [255,191,0]
    for x in range(minX,maxX+1):
        image[minY][x] = [255,191,0]
        image[maxY][x] = [255,191,0]
    return image

def markPixelRectangleBnW(list,image):
    if len(list) == 0:
        return image
    list = np.array(list)

    minY,maxY =  min(list[:,0]),max(list[:,0])
    minX,maxX =  min(list[:,1]),max(list[:,1])
    for y in range(minY,maxY+1):
        image[y][minX] = 0
        image[y][maxX] = 0
    for x in range(minX,maxX+1):
        image[minY][x] = 0
        image[maxY][x] = 0
    return image

learningRate = 0.0
BckgrSbsMOG = cv2.BackgroundSubtractorMOG()

