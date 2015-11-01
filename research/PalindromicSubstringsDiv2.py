import time
import math
# import pyximport; pyximport.install()
import PalindromicSubstringsDiv2_cython

class Timer:
    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start


class PalindromicSubstringsDiv2:
    def checkPal(self, Sin):
        if len(Sin)==1:
            return True
        N = math.ceil(len(Sin) / 2.0)
        for i in range(int(N)):
            if not Sin[i]==Sin[-i-1]:
                return False

        return True

    def count_old(self, S1, S2):
        c = 0
        for x in range (0,31457280):
            c = pow(3,3)
        return c
        # S = ''.join(S1) + ''.join(S2)
        #
        # numPal = 0
        # for iLen in range(1,len(S)+1):
        #     for i in range(len(S)-iLen+1):
        #         if self.checkPal(S[i:i+iLen]):
        #             numPal += 1
        #
        # return numPal


    def count(self, S1, S2):
        c = 0
        for x in range (0,31457280):
            c = pow(3,3)
        return c
        # S = ''.join(S1) + ''.join(S2)
        #
        # N = len(S)
        # numPal = N
        # for i in range(N):
        #     k=1
        #     #check for odd strings with i in the center
        #     while(i+k<N and i-k>=0 and S[i+k]==S[i-k]):
        #         numPal +=1
        #         k+=1
        #     k=1
        #     #check for even strings with i on the left of the double center
        #     while(i+k<N and i-k+1>=0 and S[i+k]==S[i-k+1]):
        #         numPal +=1
        #         k+=1
        #
        # return numPal



if __name__ == '__main__':
    Plist = [
            [[], ["daata"]],
            [["top"], ["coder"]],
            [["zaz"],[] ],
            [["a", "a", ""], ["a"]],
            [["a"*20] * 10, ["a"*20] * 10],
            [["a"*40] * 10, ["a"*40] * 10],
            [["a"*50] * 50, ["a"*50] * 50],
            [["a"*50] * 100, ["a"*50] * 100],
            ]


    for pi in Plist:
        p0 = pi[0]
        p1 = pi[1]
        start = time.clock()
        with Timer() as t1:
            cnt = PalindromicSubstringsDiv2_cython.count(p0, p1)
        end = time.clock()
        print 'Cython - cnt: ' + str(cnt) + ', calculated in ' + str(t1.interval),end-start

        with Timer() as t1:
            P= PalindromicSubstringsDiv2()
            # if len(p0) + len(p1) > 100:
            #     cnt = -1
            # else:
            #     cnt = P.count(p0, p1)
            cnt = P.count(p0,p1)
        print 'Python - cnt: ' + str(cnt) + ', calculated in ' + str(t1.interval)

        with Timer() as t1:
            P= PalindromicSubstringsDiv2()
            # if len(p0) + len(p1) > 20:
            #     cnt = -1
            # else:
            #     cnt = P.count_old(p0, p1)
            cnt = P.count_old(p0,p1)
        print 'Naive  - cnt: ' + str(cnt) + ', calculated in ' + str(t1.interval)
