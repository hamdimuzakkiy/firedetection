__author__ = 'hamdiahmadi'

import preprocessing
import excel
import pixelDetection as pd

stdDev, mean = pd.getStdDevAndMean('__ChoosenImage2')
clr = preprocessing.colorDetection()
res = clr.getListColorPixel(stdDev,mean)
files = open('color.txt','w')
files.truncate()
for x in res:
    files.write(str(x[0])+' '+str(x[1])+' '+str(x[2])+'\n')
files.close()

