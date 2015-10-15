__author__ = 'hamdiahmadi'

import numpy
import scipy
from sklearn import svm

print numpy.__version__
print scipy.__version__
x = [[1,2,4],[5,8,1],[2,1.5,1.8],[1,8,8],[3,1,0.6],[11,9,11]]
y = ["Api","Bukan Api","Api","Bukan Api","Api","Bukan Api"]
clf = svm.SVC(kernel = 'rbf', C = 1)
clf.fit(x,y)
print clf.predict([[6,0,2]])