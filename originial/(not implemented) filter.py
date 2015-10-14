__author__ = 'hamdiahmadi'

import file
import video
import copy

def getClock():
    MatrixX = [[0 for x in range(3)] for x in range(3)]
    MatrixX[0][0] = -1
    MatrixX[0][1] = 0
    MatrixX[0][2] = 1
    MatrixX[1][0] = -1
    MatrixX[1][1] = 0
    MatrixX[1][2] = 1
    MatrixX[2][0] = -1
    MatrixX[2][1] = 0
    MatrixX[2][2] = 1
    MatrixY = [[0 for x in range(3)] for x in range(3)]
    MatrixY[0][0] = -1
    MatrixY[0][1] = -1
    MatrixY[0][2] = -1
    MatrixY[1][0] = 0
    MatrixY[1][1] = 0
    MatrixY[1][2] = 0
    MatrixY[2][0] = 1
    MatrixY[2][1] = 1
    MatrixY[2][2] = 1
    return MatrixX,MatrixY

def execution(image, filterArr, coorx, coory):
    res = [[0 for x in range(3)] for x in range(3)]
    clockX,clockY = getClock()
    ans = 0
    for y in range(0,len(res)):
        for x in range(0,len(res[y])):
            if coorx + clockX[y][x] == -1 or coorx + clockX[y][x] == len(image[0]) or coory + clockY[y][x] == -1 or coory + clockY[y][x] == len(image) :
                pass
            else :
                ans = ans + image[coory + clockY[y][x]][coorx + clockX[y][x]]*filterArr[y][x]
    #         try :
    #             print coory,coorx, coory + clockY[y][x], coorx + clockX[y][x], filterArr[y][x], image[coory + clockY[y][x]][coorx + clockX[y][x]]
    #         except :
    #             print coory,coorx, coory + clockY[y][x], coorx + clockX[y][x], filterArr[y][x], 0
    #     print "===="
    # print ans,"-----"
    return ans

def filter(image,const, filterArr):
    res = video.copyFile(image)
    # res[0][0] = 1
    # # print res[0][0]
    # print image[1][1]
    # print res
    # print image
    # return
    # image = [[2 for x in range(5)] for x in range(4)]
    # res = copy.deepcopy(image)
    for y in range(0,len(image)):
        for x in range(0,len(image[y])):
            res[y][x] = execution(image, filterArr, x, y)/const
            # res[y][x] = execution(image, filterArr, x, y)
    return res

def getFilter(strings):
    if strings == 'Low':
        return 16,[[1,2,1],[2,4,2],[1,2,1]]
    else :
        return 1,[[-1,-1,2],[-1,2,-1],[2,-1,-1]]
        return 3,[[-1,-1,2],[-1,2,-1],[2,-1,-1]]

fileName = '../../204_METANA.jpg'
fileName = '../../0.png'
Image = video.toGray(video.readImage(fileName))
video.saveFrame("Images.png",Image)
# cons,filt = getFilter('High')
# Image = filter(Image, cons,filt)
# print Image
# video.saveFrame("muzakkiy2.png",Image)
#
