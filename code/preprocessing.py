__author__ = 'hamdiahmadi'
import numpy as np
import cv2
import copy
import os

class File:

    def __init__(self):
        pass

    def saveImage(self, name, image):
        return cv2.imwrite(name,image)

    def readFolder(self,path):
        return os.listdir(path)

    def getCountFrame(self, video):
        return video.get(7)

    def readVideo(self, video):
        return video.read()

    def isOpened(self, video):
        return video.isOpened()

    def readImage(self, path):
        return cv2.imread(path)

    def waitVideo(self, sec):
        return cv2.waitKey(sec)

    def showVideo(self, name, image):
        return cv2.imshow(name,image)

    def closeVideo(self, video):
        return video.release()

    def openVideo(self, path):
        return cv2.VideoCapture(path)

class Data:

    def __init__(self):
        pass

    #return array dengan 8 tetangga sesuai jarum jam
    def getClockwise(self):
        clocks = []
        clocks.append([-1,-1])
        clocks.append([-1,0])
        clocks.append([-1,1])
        clocks.append([0,-1])
        clocks.append([0,1])
        clocks.append([1,-1])
        clocks.append([1,0])
        clocks.append([1,1])
        return clocks

    def getClockwise4(self):
        clocks = []
        clocks.append([-1,0])
        clocks.append([0,-1])
        clocks.append([0,1])
        clocks.append([1,0])
        return clocks

    def getDatasetPixel(data):
        arr = []
        res = np.where(data != [0,0,0])
        for x in range(0,len(res[0]),3) :
            arrays = data[res[0][x]][res[1][x]][0],data[res[0][x]][res[1][x]][1],data[res[0][x]][res[1][x]][2]
            arr.append(arrays)
        return arr

    #return nilai dari probabilitas gaussian
    #standard deviasi , mean, data berisi nilai tunggal
    def getGaussianProbability(self, data, standard_deviasi, mean):
        data = float(data)
        standard_deviasi = float(standard_deviasi)
        mean = float(mean)
        result = pow((data-mean),2)
        div = 2*pow(standard_deviasi,2)
        exp = np.exp(-result/div)
        result = standard_deviasi*np.sqrt(2*np.pi)
        result = 1/result
        return result* exp

    #return normal range 0 - 1
    def getNormalRange(self, list_data):
        max = float(np.max(list_data))
        min = float(np.min(list_data))

        result = []
        for x in list_data:
            try :
                tmp = (float(x)-min)/(max-min)
            except:
                tmp = 0
            float('%.2f' % round(tmp))
            result.append(tmp)
        return result

    #return maximal value dari list data
    def getMaxList(self, list_data):
        return np.max(list_data)

    #return minimal value dari list data
    def getMinList(self, list_data):
        return np.min(list_data)

    def sumArray(self, list_data):
        return np.sum(list_data,axis=0)

    def getDistance(self, point1, point2):
        return np.sqrt(pow(point1[0]-point2[0],2)+pow(point1[1]-point2[1],2))

class ImageProcessing:
    def __init__(self):
        pass

    def readImage(self,path):
        return cv2.imread(path)

    #return RGB image ke Gray Image
    def getRGBtoGray(self,image):
        return cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)

    #return Gaussian image dengan filter ( int ) bluring
    def getGaussianFilter(self,gray_image,filter):
        return cv2.blur(gray_image,(filter,filter))

    #return image dengan down-sampled image
    def getDownSize(self,image):
        return cv2.pyrDown(image)

    #return image dengan up-sampled image
    def getUpSize(self,image):
        return cv2.pyrUp(image)

class ColorDetection(Data,File,ImageProcessing):

    def __init__(self):
        pass

    # return threshold untuk range warna api
    def getThreshold(self):
        return 5*pow(10,-9)

    # return Array dengan index R G B dimana array tersebut memiliki nilai True & False sebagai referensi apakah Api atau Bukan
    def getFireArray(self,path):
        lists = [[[False for k in xrange(256)] for j in xrange(256)]for i in xrange(256)]
        data = open(path,'r')
        for x in data:
            color = (x.split('\n')[0]).split(' ')
            lists[int(color[0])][int(color[1])][int(color[2])] = True
        return lists

    # return R G B yang masuk dalam range warna api
    def getListColorPixel(self,list_standard_deviasi, list_mean):
        res = []
        threshold = self.getThreshold()
        for B in range(0,256):
            for G in range(B,256):
                for R in xrange(G,256):
                    if Data.getGaussianProbability(self,B, list_standard_deviasi[0], list_mean[0])* Data.getGaussianProbability(self,G, list_standard_deviasi[1], list_mean[1])* Data.getGaussianProbability(self,R, list_standard_deviasi[2], list_mean[2]) > threshold:
                        res.append([B,G,R])
        return res

    # return candidate pixel
    def getColorCandidatePixel(self, list_candidate, image, color_dataset):
        true_pixel = []
        false_pixel = []
        for x in range(0,len(list_candidate[0])):
            data = image[list_candidate[0][x]][list_candidate[1][x]]
            B,G,R = data[0],data[1],data[2]
            if color_dataset[B][G][R] == True:
                true_pixel.append([list_candidate[0][x],list_candidate[1][x]])
            else :
                false_pixel.append([list_candidate[0][x],list_candidate[1][x]])
        return true_pixel,false_pixel

    def getColorImage(image):
        arr = []
        res = np.where(image != [0,0,0])
        for x in range(0,len(res[0]),3) :
            arrays = image[res[0][x]][res[1][x]][0],image[res[0][x]][res[1][x]][1],image[res[0][x]][res[1][x]][2]
            arr.append(arrays)
        return arr

    def getStdDevAndMean(self,path):
        list_file = File.readFolder(self,path)        
        R = []
        G = []
        B = []
        for x in list_file:
            image = ImageProcessing.readImage(self,path+'/'+x)
            r = np.array(image[:,:,2]).ravel()
            g = np.array(image[:,:,1]).ravel()
            b = np.array(image[:,:,0]).ravel()
            R += (r.tolist())
            G += (g.tolist())
            B += (b.tolist())
        mean = []   
        mean.append(np.average(B))
        mean.append(np.average(G))
        mean.append(np.average(R))
        standard_deviasi = []
        standard_deviasi.append(np.std(B))
        standard_deviasi.append(np.std(G))
        standard_deviasi.append(np.std(R))
        return standard_deviasi, mean

class Luminance(Data,ImageProcessing):

    def __init__(self):
        pass

    #return luminance image1 dan image2
    def getLuminance(self,gaussian_luminance1,gaussian_luminance2):
        max_7,max_13 = Data.getMaxList(self,gaussian_luminance1),Data.getMaxList(self,gaussian_luminance2)
        min_7,min_13 = Data.getMinList(self,gaussian_luminance1),Data.getMinList(self,gaussian_luminance2)
        if (max_7-min_7 == 0):
            max_7+=1
        if (max_13-min_13 == 0):
            max_13+=1
        gaussian_luminance1-=min_7
        gaussian_luminance2-=min_13
        gaussian_luminance1*=(255/(max_7-min_7))
        gaussian_luminance2*=(255/(max_13-min_13))
        gaussians = cv2.add((gaussian_luminance1),(gaussian_luminance2))
        return gaussians

    #return luminance 2 gray image
    def getLuminanceImageGray(self,gray_image):
        return gray_image

    #return luminance luminance image dengan gaussian filter 7 dan gaussian filter 13
    def getLumiananceImage(self,gray_image):
        gaussian_lumianance_13 = ImageProcessing.getGaussianFilter(self,copy.copy(gray_image),13)
        gaussian_lumianance_7 = ImageProcessing.getGaussianFilter(self,copy.copy(gray_image),7)
        return self.getLuminance(gaussian_lumianance_7,gaussian_lumianance_13)

class Intensity(Data):

    def __init__(self):
        pass

    #return range image dengan pelebaran nilai contan dari titik ekstrim
    def getRangeConstant(self, image, list_candidate, constanta):
        min_y,min_x = Data.getMinList(self,list_candidate[0]),Data.getMinList(self,list_candidate[1])
        max_y,max_x = Data.getMaxList(self,list_candidate[0]),Data.getMaxList(self,list_candidate[1])

        constanta-=1
        max_range = min(max_x - min_x, max_y - min_y)
        len_y = max_range
        len_x = max_range

        if min_y - int(len_y*constanta) < 0:
            min_y = 0
        else :
            min_y = min_y - int(len_y*constanta)
        if min_x - int(len_x*constanta) < 0:
            min_x = 0
        else :
            min_x = min_x - int(len_x*constanta)
        if int(max_y+len_y*constanta)>=len(image):
            max_y = int(len(image)-1)
        else:
            max_y = int(max_y+len_y*constanta)
        if int(max_x+len_x*constanta)>=len(image[0]):
            max_x = int(len(image[0])-1)
        else:
            max_x = int(max_x+len_x*constanta)

        return min_y,min_x,max_y,max_x

    #return candidate pixel dengan kosndisi dimana objeck tersebut lebih terang dari sekelilingnya
    def getLuminanceCandidatePixel(self, image, list_candidate, region):
        true_pixel = []
        false_pixel = []
        threshold = dict()
        list_region = np.unique(region)
        for x in range(1,len(list_region)):
            lists = np.where(region == x)
            min_y,min_x = Data.getMinList(self,lists[0]),Data.getMinList(self,lists[1])
            max_y,max_x = Data.getMaxList(self,lists[0]),Data.getMaxList(self,lists[1])
            candidate_object = copy.copy(image)[min_y:max_y,min_x:max_x]
            minY,minX,maxY,maxX = self.getRangeConstant(image,lists,1.5)
            around_object = copy.copy(image)[minY:maxY,minX:maxX]
            sum_candidate = np.sum(candidate_object)
            sum_arround = np.sum(around_object)
            try:
                threshold[x] = (sum_arround-sum_candidate)/((len(around_object)*len(around_object[0]))-(len(candidate_object)*len(candidate_object[0]))+1)
            except:
                threshold[x] = 255
        for x in list_candidate:
            coor_y = x[0]
            coor_x = x[1]
            if image[coor_y][coor_x] >= threshold[region[coor_y][coor_x]]:
                true_pixel.append([coor_y,coor_x])
            else:
                false_pixel.append([coor_y,coor_x])
        return true_pixel,false_pixel

    #return candidate pixel dengan melihat besarnya berubahan pixel
    def getDifferenceCandidatePixel(self, list_image, list_candidate):
        truePixel = []
        falsePixel = []
        for x in list_candidate:
            arr = []
            for y in list_image:
                arr.append(y[x[0]][x[1]])
            res = float(np.std(arr))
            if (res > 2 and res < 40):
                truePixel.append([x[0],x[1]])
            else:
                falsePixel.append([x[0],x[1]])
        return truePixel,falsePixel

class Moving(Intensity,ImageProcessing):

    def __init__(self):
        try:
            self.BckgrSbsMOG = cv2.BackgroundSubtractorMOG()
        except:
            # self.BckgrSbsMOG = cv2.BackgroundSubtractorMOG()
            self.BckgrSbsMOG = cv2.createBackgroundSubtractorMOG2()

    #return learning rate
    def getLearningRate(self):
        return 0.0005

    #return index moving foreground ( moving object )
    def getMovingForeGround(self, image):
        return self.BckgrSbsMOG.apply(image,learningRate = self.getLearningRate())

    #return image moving foreground ( moving object )
    def getMovingCandidatePixel(self, moving_frame):
        listY,listX = np.where( moving_frame == 255 )
        return np.vstack((listY,listX))

    #marking pixel
    def markingFire(self, list_fire, image, constanta):
        if len(list_fire) == 0:
            return image

        list = np.array(list_fire)
        min_y,max_y =  min(list[:,0]),max(list[:,0])
        min_x,max_x =  min(list[:,1]),max(list[:,1])

        distance_y = int((max_y-min_y)/2)*constanta
        distance_x = int((max_x-min_x)/2)*constanta
        center_point = [int((max_y+min_y)*constanta/2),int((max_x+min_x)*constanta/2)]

        min_y,min_x,max_y,max_x = center_point[0]-distance_y, center_point[1] - distance_x, center_point[0] + distance_y, center_point[1] +distance_x

        for y in range(min_y,max_y+1):
            image[y][min_x] = [255,191,0]
            image[y][max_x] = [255,191,0]
        for x in range(min_x,max_x+1):
            image[min_y][x] = [255,191,0]
            image[max_y][x] = [255,191,0]
        return image

    def markingFire2(self, list_fire, image):
        if len(list_fire) == 0:
            return image

        for x in list_fire:
            coory,coorx = x[0],x[1]
            image[coory][coorx] = [255,191,0]
        return image

class RegionGrowing(Data,ImageProcessing,File):

    def __init__(self):
        pass

    #return candidate pixel dengan mencari warna region dari objek
    def getFilterSizeRegion(self,list_candidate,region):
        true_pixel = []
        false_pixel = []
        list_region = np.unique(region)
        threshold = dict()
        for x in range(1,len(list_region)):
            lists = np.where(region == x)
            if len(lists[0]) > 1*len(region)*len(region[0])/100:
                threshold[x] = True
            else :
                threshold[x] = False
        for x in list_candidate:
            coor_y = x[0]
            coor_x = x[1]
            if threshold[region[coor_y][coor_x]] == True:
                true_pixel.append([coor_y,coor_x])
            else :
                false_pixel.append([coor_y,coor_x])
        return true_pixel,false_pixel

    #return candidate pixel dengan melihat pergerakan dari posisi titik tengah objeck tersebut
    def getMovingPointCandidatePixel(self, list_region_growing, list_candidate):
        true_pixel = []
        false_pixel = []
        ref = []
        for x in list_region_growing:
            res = dict()
            list_region = np.unique(x)
            for val in list_region :
                if val == 0:
                    continue
                reg = (np.where(x == val))
                minY,minX,maxY,maxX = np.min(reg[0]),np.min(reg[1]),np.max(reg[0]),np.max(reg[1])
                res[val] = [(maxY-minY)/2,(maxX-minX)/2]
            ref.append(res)
        for x in list_candidate:
            lists = []
            coor_y = x[0]
            coor_x = x[1]
            for y in range (0,len(list_region_growing)):
                val = list_region_growing[y][coor_y][coor_x]
                if val == 0:
                    continue
                lists.append(ref[y][val])
            res = 0
            cnt = 0
            for x in range(0,len(lists)-1):
                sum = pow((lists[x][0]-lists[x+1][0]),2)+pow((lists[x][1]-lists[x+1][1]),2)
                res = res + np.sqrt(sum)
                cnt+=1
            if res != 0:
                res = res/cnt
            if  res > 1:
                true_pixel.append([coor_y,coor_x])
            else :
                false_pixel.append([coor_y,coor_x])
        return true_pixel,false_pixel

    def getMovingPointCandidatePixel2(self, list_region_growing, list_candidate):
        true_pixel = []
        false_pixel = []
        ref = []
        for x in list_region_growing:
            res = dict()
            list_region = np.unique(x)
            for val in list_region :
                if val == 0:
                    continue
                reg = (np.where(x == val))
                minY,minX,maxY,maxX = np.min(reg[0]),np.min(reg[1]),np.max(reg[0]),np.max(reg[1])
                res[val] = [(maxY-minY)/2,(maxX-minX)/2]
            ref.append(res)
        result_dict = dict()
        for x in ref[len(list_region_growing)-1]:
            res = 0
            frame_number = len(list_region_growing)-1
            cur_region = x
            tmp = copy.copy(list_region_growing[len(list_region_growing)-1])*100000
            Flag = False
            for y in range(len(list_region_growing)-2,-1,-1):
                matrix_adding = np.add(tmp,list_region_growing[y])
                max = 0
                next_cur_region = x
                for z in ref[y]:
                    size = len(np.where(matrix_adding == 100000*cur_region+z)[0])
                    if size > max :
                        max = size
                        next_cur_region = z
                        Flag = True
                if Flag == True:
                    next_point = ref[y][next_cur_region]
                    curent_point = ref[frame_number][cur_region]
                    res+=Data.getDistance(self, curent_point, next_point)
                    tmp = copy.copy(list_region_growing[y])*100000
                    cur_region = next_cur_region
                    frame_number = y
                    Flag = False
            if res/10 > 1:
                result_dict[x] = True
            else :
                result_dict[x] = False
        for x in list_candidate:
            val = list_region_growing[len(list_region_growing)-1][x[0]][x[1]]
            if result_dict[val] == True:
                true_pixel.append([x[0],x[1]])
            else :
                true_pixel.append([x[0],x[1]])
        return true_pixel,false_pixel

    #return floodfill image
    def doFloodFill(self, gray_image ,result_image ,is_visit, stack, region_number, color_dataset, original_image):
        clocks = Data.getClockwise(self)
        while len(stack) != 0:
            coory,coorx = stack[0]
            stack.pop(0)
            result_image[coory][coorx] = 255
            data = original_image[coory][coorx]
            B,G,R = data[0],data[1],data[2]
            for x in clocks:
                try :
                    if is_visit[coory+x[0]][coorx+x[1]] == 0 and color_dataset[B][G][R] == True :
                        is_visit[coory+x[0]][coorx+x[1]] = region_number
                        stack.append([coory+x[0],coorx+x[1]])
                except :
                    pass
        return result_image,is_visit
    #return floodfill image
    def getRegionGrowing(self, list_candidate, images, color_dataset,counter):
        gray_image = ImageProcessing.getRGBtoGray(self,images)
        is_visit = gray_image*0
        result_image = copy.copy(gray_image)
        region_number = 0
        for x in list_candidate:
            coor_y = x[0]
            coor_x = x[1]
            if is_visit[coor_y][coor_x] == 0:
                stack = []
                region_number+=1
                stack.append([coor_y,coor_x])
                is_visit[coor_y][coor_x] = region_number
                result_image, is_visit = self.doFloodFill( gray_image, result_image, is_visit, stack, region_number, color_dataset, images)
        return is_visit