__author__ = 'hamdiahmadi'

import pixelDetection as pd
import excel as ex

fileName = '../../../corped/__ChoosenImage2'
data = pd.getPixelColorList(fileName)
ex.save(data,'data1')