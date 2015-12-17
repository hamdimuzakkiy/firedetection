__author__ = 'hamdiahmadi'

import preprocessing

clr = preprocessing.ColorDetection()
stdDev, mean = clr.getStdDevAndMean('-dataset-fire_image')

res = clr.getListColorPixel(stdDev,mean)
files = open('color2.txt','w')
files.truncate()
for x in res:
    files.write(str(x[0])+' '+str(x[1])+' '+str(x[2])+'\n')
files.close()

