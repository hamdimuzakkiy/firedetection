__author__ = 'hamdiahmadi'
import classification as cls

import excel
import moving as mv
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
            #get curent frame
            currentFrame = File.readVideo(videoFile)[1]
            #compres image
            while (len(currentFrame)>150):
                if (len(currentFrame)<=300):
                    currentFrame2 = copy.copy(currentFrame)
                currentFrame = ImageProcessing.getDownSize(currentFrame)
            counter+=1

            # step 1 get moving pixel
            movingFrame = Moving.getMovingForeGround(copy.copy(currentFrame))
            movingPixel = Moving.getMovingCandidatePixel(movingFrame)


            # step 2 candidate pixel ( color probability )
            ColorCandidatePixel = Color.getColorCandidatePixel(copy.copy(movingPixel), copy.copy(currentFrame), list_color)

            #region growing
            region = RegionGrowing.getRegionGrowing(ColorCandidatePixel[0], copy.copy(currentFrame),list_color,counter)

            # step 3 region candidate pixel ( region size )
            sizeRegionCandidatePixel = RegionGrowing.getFilterSizeRegion(copy.copy(ColorCandidatePixel[0]),copy.copy(region))

            #preparing classification
            grayImage = ImageProcessing.getRGBtoGray(currentFrame2)
            LL,(HL,LH,HH) = wv.toWavelet(copy.copy(grayImage))

            list_wavelet.append([HL,LH,HH])
            if (counter<=10):
                continue
            list_wavelet.pop(0)

            FinalCandidatePixel = cls.doClassification(classifier,copy.copy(sizeRegionCandidatePixel[0]),list_wavelet)

            fireFrameImage = (ImageProcessing.getUpSize(Moving.markingFire(FinalCandidatePixel[0],currentFrame2, 2)))
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

        except ValueError:
            print "Time : ",time.time() - starts
            return (fireFrame)/float(AllFrame)
    print "Time : ",time.time() - starts
    return (fireFrame)/float(AllFrame)


if __name__ == '__main__':
    file = 'api_cars.avi'
    file = 'api_doll_house2.avi'
    file = 'api_dora.avi'
    file = 'api_hutan_besar1.avi'
    file = 'api_kayu_hutan_besar1.avi'
    file = 'api_kayu_hutan1.avi'
    file = 'api_kayu1.avi'
    file = 'api_kayu2.avi'
    file = 'api_kertas1.avi'
    file = 'api_kertas2.avi'

    file = 'api_ladang1.avi'
    file = 'api_mainan1.avi'
    file = 'api_mainan2.avi'
    # file = 'api_mobil1.avi'
    # file = 'api_mobil2.avi'
    # file = 'api_rc2.avi'
    # file = 'api_ruang_tamu1.avi'
    # file = 'api_senter1.avi'
    # file = 'api_senter2.avi'
    # file = 'api_terjun.avi'
    #
    # file = 'api_tol2.avi'
    # file = 'api_truck1.avi'
    # file = 'api_truck2.avi'
    # file = 'api_truck3.avi'
    # file = 'non_api_anak_kecil1.avi'
    # file = 'non_api_anak_kecil2.avi'
    # file = 'non_api_anak_kecil3.avi'
    # file = 'non_api_bertemu.avi'
    # file = 'non_api_hamdi2.avi'
    # file = 'non_api_jaket_merah.avi'
    #
    # file = 'non_api_jalan_malam1.avi'
    # file = 'non_api_jalan_malam2.avi'
    # file = 'non_api_jalan_raya1.avi'
    # file = 'non_api_jalan_raya2.avi'
    # file = 'non_api_jalan_raya3.avi'
    # file = 'non_api_ke_mobil1.avi'
    # file = 'non_api_ke_mobil2.avi'
    # file = 'non_api_ke_mobil3.avi'
    # file = 'non_api_kecelakaan1.avi'
    # file = 'non_api_kecelakaan2.avi'

    # file = 'non_api_kecelakaan3.avi'
    # file = 'non_api_las_vegas1.avi'
    # file = 'non_api_parkiran1.avi'
    # file = 'non_api_parkiran2.avi'
    # file = 'non_api_parkiran3.avi'
    # file = 'non_api_pencuri1.avi'
    # file = 'non_api_pencuri3.avi'
    # file = 'non_api_tauran1.avi'
    # file = 'non_api_tauran2.avi'
    # file = 'non_api_tauran3.avi'
    #
    # file = 'non_api_televisi1.avi'
    # file = 'non_api_televisi2.avi'
    # file = 'non_api_tembak3.avi'

    path = '../../dataset/fix_data/'
    print file
    fileName = path+file

    File = preprocessing.File()
    videoFile = File.openVideo(fileName)
    res = readingVideo(videoFile)*100
    print "Acc : ",res,' %'
    report = []
    report.append(file)
    for y in res:
        report.append(y)
    excel.writeAccuracy('-file-laporan/final_akurasi_5&5x10^-9.xls',report)

    print "Moving | Color | Size Region | Classififcation"
    File.closeVideo(videoFile)