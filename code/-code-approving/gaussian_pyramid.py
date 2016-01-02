__author__ = 'hamdiahmadi'

import cv2
import numpy as np

def initFilter():
    coef = 256
    arr = []
    arr.append([1,4,6,4,1])
    arr.append([4,16,24,16,4])
    arr.append([6,24,36,25,6])
    arr.append([4,16,24,16,4])
    arr.append([1,4,6,4,1])
    return coef,arr

def getFilter(image):
    res = np.ndarray(shape=(len(image),len(image[0]),3))
    coef,filter = initFilter()
    for row in range(0,len(image)):
        for col in range(0,len(image[row])):
            for channel in range(0,len(image[row][col])):
                tmp = 0
                for y in range(0,len(filter)):
                    for x in range(0,len(filter)):
                        try:
                            tmp+= image[row+y-2][col+x-2][channel]*filter[y][x]
                        except:
                            tmp+= image[row-y][col-x][channel]*filter[y][x]
                res[row][col][channel] = tmp/coef
    return res

def downSampled(image):
    image = getFilter(image)
    res = np.ndarray(shape=(len(image)/2,len(image[0])/2,3))
    for row in range(0,len(res)):
        for col in range(0,len(res[row])):
            for channel in range(0,len(res[row][col])):
                res[row][col][channel] = image[row*2][col*2][channel]
    return res

if __name__ == '__main__':
    image = cv2.imread('api-boneka_dora.avi71.png')
    res = downSampled(image)
    cv2.imwrite('new.png',res)