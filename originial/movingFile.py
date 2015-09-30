__author__ = 'hamdiahmadi'
import os
import decimal
import numbers

if __name__ == '__main__':
    file = open('list.txt','r')
    listDir = file.readlines()
    print len(listDir)
    for x in listDir:
        print isinstance(x, (int, long, float, complex))