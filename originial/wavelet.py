__author__ = 'hamdiahmadi'
import pywt
import video

def toWavelet(image):
    return pywt.dwt2(image,'db4')

# fileName = '../../13732_1062770107321_3577169_n.jpg'
# fileName = '../../60.png'
# Image = video.toGray(video.readImage(fileName))
# print len(Image),len(Image[0])
# LL,(LH,HL,HH) = pywt.dwt2(Image, 'db1')
#
# video.saveFrame('HH1.png',abs(HH))
# video.saveFrame('LH1.png',abs(LH))
# video.saveFrame('HL1.png',abs(HL))
# video.saveFrame('LL1.png',abs(LL))