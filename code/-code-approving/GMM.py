__author__ = 'hamdiahmadi'

import cv2
import numpy as np
import copy

def probability(x,mean,stdev):
    bawah = float(1)/np.sqrt(2*np.pi*stdev)
    atas = np.exp(-(x-mean)*(x-mean)*stdev/2)
    return atas/bawah

image = cv2.imread('1.png')
image = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)

gaussian = []
for x in range(0,3):
    gaussian.append(np.ndarray(shape=(len(image),len(image[0]),3)))

for row in range(0,len(image)):
    for col in range(0,len(image[row])):
        for g in gaussian:
            g[row][col][0] = float(1)/float(len(gaussian)) # w
            g[row][col][1] = image[row][col] # mean
            g[row][col][2] = 20 # deviasi
for img in range(2,177):
    threshold = 0.5
    learning_rate = 0.002
    next_image = cv2.imread(str(img)+'.png')
    next_image = cv2.cvtColor(next_image,cv2.COLOR_RGB2GRAY)
    res = copy.copy(next_image)*0
    for row in range(0,len(next_image)):
        for col in range(0,len(next_image[row])):
            dtype = [('k', int), ('w', float)]
            values = [(0,gaussian[0][row][col][0]),(1,gaussian[1][row][col][0]),(2,gaussian[2][row][col][0])]
            arr = np.array(values,dtype=dtype)
            arr = np.sort(arr,order='w')
            tmp = 0
            cnt = 0
            for x in arr:
                tmp+=x[1]
                cnt+=1
                if tmp > threshold:
                    break
            first = True
            match = False
            for x in range(0,cnt):
                indeks = arr[x][0]
                if abs(next_image[row][col]-gaussian[indeks][row][col][1]) > gaussian[indeks][row][col][2]*2.5:
                    if first == True:
                        gaussian[indeks][row][col][0] = (1-learning_rate) * gaussian[indeks][row][col][0]+learning_rate
                    else :
                        gaussian[indeks][row][col][0] = (1-learning_rate) * gaussian[indeks][row][col][0]
                    prob = probability(next_image[row][col],gaussian[indeks][row][col][1],gaussian[indeks][row][col][2])
                    gaussian[indeks][row][col][1] = (1-learning_rate)*gaussian[indeks][row][col][1]+prob*next_image[row][col]
                    gaussian[indeks][row][col][2] = (1-learning_rate)*gaussian[indeks][row][col][2]+prob*pow(next_image[row][col]-gaussian[indeks][row][col][1],2)
                    res[row][col] = 255
                    match = False
                    break
            if match == False:
                indeks = arr[cnt-1][0]
                gaussian[indeks][row][col][2] = 30
                gaussian[indeks][row][col][1] = next_image[row][col]
                gaussian[indeks][row][col][0] = 0.00001
    cv2.imwrite('_'+str(img)+'.png',res)
