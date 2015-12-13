__author__ = 'hamdiahmadi'
import os

def openFile(path):
    return open(path,'r')

def readFile(file):
    return file.read()

def saveFile(name,location,data,extension):
    file = open(location+'/'+str(name)+extension,'w')
    file.write(data)
    return

def getListFolder(path):
    return os.listdir(path)