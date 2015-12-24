__author__ = 'hamdiahmadi'
import classification as cls

import excel
import preprocessing as preprocessing
import wavelet as wv
import time
import copy
import numpy


def readingVideo(videoFile):
    Color = preprocessing.ColorDetection()
    File = preprocessing.File()
    RegionGrowing = preprocessing.RegionGrowing()
    ImageProcessing = preprocessing.ImageProcessing()
    Moving = preprocessing.Moving()

    stdDev, mean = Color.getStdDevAndMean('-dataset-fire_image')
    print "Stdev : "+str(stdDev), "Mean : "+str(mean)
    print "Video Frame : ",File.getCountFrame(videoFile)
    print "Video Size : ",len(File.readVideo(videoFile)[1]),len(File.readVideo(videoFile)[1][0])

    classifier = cls.getClassifier('-file-datatraining/TA.xls')
    fireFrame = numpy.array([0,0,0,0])
    list_wavelet = []
    list_color = Color.getFireArray('color_5x10^-9.txt')
    AllFrame = 0
    counter = 0

    starts = time.time()
    while(File.isOpened(videoFile)):
        try :
            currentFrame = File.readVideo(videoFile)[1]
            if len(currentFrame) == 0:
                return
            currentFrame2 = copy.copy(currentFrame)
            currentFrame = ImageProcessing.getDownSize(currentFrame)
            counter+=1
            movingFrame = Moving.getMovingForeGround(copy.copy(currentFrame))
            movingPixel = Moving.getMovingCandidatePixel(movingFrame)
            ColorCandidatePixel = Color.getColorCandidatePixel(copy.copy(movingPixel), copy.copy(currentFrame), list_color)
            region = RegionGrowing.getRegionGrowing(ColorCandidatePixel[0], copy.copy(currentFrame),list_color,counter)
            sizeRegionCandidatePixel = RegionGrowing.getFilterSizeRegion(copy.copy(ColorCandidatePixel[0]),copy.copy(region))
            grayImage = ImageProcessing.getRGBtoGray(currentFrame2)
            LL,(HL,LH,HH) = wv.toWavelet(copy.copy(grayImage))
            list_wavelet.append([HL,LH,HH])
            if (counter<=10):
                continue
            list_wavelet.pop(0)
            FinalCandidatePixel = cls.doClassification(classifier,copy.copy(sizeRegionCandidatePixel[0]),list_wavelet)
            fireFrameImage = ((Moving.markingFire(FinalCandidatePixel[0],currentFrame2, 2)))
            File.showVideo('Final',fireFrameImage)

            if len(movingPixel[0])>0:
                fireFrame[0]+=1
            if len(ColorCandidatePixel[0])>0:
                fireFrame[1]+=1
            if len(sizeRegionCandidatePixel[0])>0:
                fireFrame[2]+=1
            if len(FinalCandidatePixel[0])>0:
                fireFrame[3]+=1

            AllFrame+=1

            File.waitVideo(1)

        except :
            print "Time : ",time.time() - starts
            return (fireFrame)/float(AllFrame),File.getCountFrame(videoFile),time.time() - starts
    print "Time : ",time.time() - starts
    return (fireFrame)/float(AllFrame),File.getCountFrame(videoFile),time.time() - starts


if __name__ == '__main__':
    file = 'api-boneka_dora.avi'
    file = 'api-kayu.avi'
    file = 'api-kayu2.avi'
    file = 'api-kebakaran_hutan.avi'
    file = 'api-kebakaran_hutan2.avi'
    file = 'api-kebakaran_hutan3.avi'
    file = 'api-kebakaran_ladang.avi'
    file = 'api-kebakaran_mobil.avi'
    file = 'api-kebakaran_mobil2.avi'
    file = 'api-kebakaran_tol.avi'

    file = 'api-kebakaran-truck.avi'
    file = 'api-kebakaran-truck2.avi'
    file = 'api-kebakaran-truck3.avi'
    file = 'api-kertas.avi'
    file = 'api-kertas2.avi'
    file = 'api-miniatur_mainan.avi'
    file = 'api-mobil_mainan.avi'
    file = 'api-orang_terjun.avi'
    file = 'api-pesawat_mainan.avi'
    file = 'api-pesawat_mainan2.avi'

    file = 'api-ruang_tamu.avi'
    file = 'api-rumah_mainan.avi'
    file = 'api-senter.avi'
    file = 'api-senter2.avi'
    file = 'non_api-anak_kecil.avi'
    file = 'non_api-anak_kecil2.avi'
    file = 'non_api-anak_kecil3.avi'
    file = 'non_api-bertemu.avi'
    file = 'non_api-jaket_merah.avi'
    file = 'non_api-jalan_malam.avi'

    file = 'non_api-jalan_malam2.avi'
    file = 'non_api-jalan_raya.avi'
    file = 'non_api-jalan_raya2.avi'
    file = 'non_api-jalan_raya3.avi'
    file = 'non_api-kecelakaan.avi'
    file = 'non_api-kecelakaan2.avi'
    file = 'non_api-kecelakaan3.avi'
    file = 'non_api-kerusuhan.avi'
    file = 'non_api-kerusuhan2.avi'
    file = 'non_api-kerusuhan3.avi'
    #
    file = 'non_api-las_vegas.avi'
    file = 'non_api-manuju_mobil.avi'
    file = 'non_api-manuju_mobil2.avi'
    file = 'non_api-manuju_mobil3.avi'
    file = 'non_api-parkiran.avi'
    file = 'non_api-parkiran2.avi'
    file = 'non_api-parkiran3.avi'
    file = 'non_api-pencuri.avi'
    file = 'non_api-pencuri2.avi'
    file = 'non_api-penembakan.avi'

    file = 'non_api-serbet.avi'
    file = 'non_api-televisi.avi'
    file = 'non_api-televisi2.avi'
    #
    path = '../../dataset/fix_data/'
    print file
    fileName = path+file

    File = preprocessing.File()
    videoFile = File.openVideo(fileName)
    res, frameCounter, times = readingVideo(videoFile)
    res*=100
    print "Acc : ",res,' %'
    report = []
    report.append(file)
    for y in res:
        report.append(y)
    report.append('')
    report.append(frameCounter)
    report.append(times)
    excel.writeAccuracy('-file-laporan/final_akurasi_5&10^-9&polynomial.xls',report)
    print "Moving | Color | Size Region | Classififcation"
    File.closeVideo(videoFile)