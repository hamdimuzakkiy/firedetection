__author__ = 'hamdiahmadi'
import data as dt


def getMyu(data):
    sum = 0
    sumIncrement = 0
    for x in range(0,len(data)):
        sum+=data[x]
        sumIncrement+=((x+1)*data[x])
    return sum, sumIncrement, float(float(sumIncrement)/float(sum))

def getVariance(data,Myu,sums):
    sum = 0
    print data
    for x in range(0,len(data)):
        sum+=(dt.getPower(float(x+1)-float(Myu),2)*float(data[x]))
    return float(sum)/float(sums)

def getLuminancePixel(List, ListImage):
    result = []
    for x in List:
        res = []
        for cnt in range(0,len(ListImage)):
            img = ListImage[cnt]
            val = img[x[0]][x[1]]
            res.append(val)

        sum,sumIncrement,Myu = getMyu(res)
        variance = getVariance(res,Myu,sum)
        if (variance>8):
            result.append([x[0],x[1]])
    return result

def setData():
    res = []
    for x in range(0,10):
        res.append(0)
    return res

def edge(List, ListImage):
    result = []
    for x in List:
        dct = 0
        res = []
        for cnt in range(0,len(ListImage)):
            img = ListImage[cnt]
            val = img[x[0]][x[1]]
            res.append(val)
            if val == 255 :
                dct+=1
        if dct > 3:
            result.append([x[0],x[1]])
    return result

def getLuminancePixel2(list, image):
    res = []
    threshold = dt.sum2D(image)/(len(image)*len(image[0]))
    for x in list:
        if (image[x[0]][x[1]]>=threshold):
            res.append(x)
    return res
