#!/usr/bin/python
import numpy as np
import cv2 as cv
import glob
import threading
from multiprocessing import Pool
path ='/home/evilblubb/100EOS5D/'
dic=[]
def resizer(file):
    img = cv.UMat(cv.imread(file))
    res = cv.resize(img,None, fx =0.5, fy=0.5, interpolation=cv.INTER_CUBIC)
    name=file.split('/')[-1]
    print(name)
    cv.imwrite('/home/evilblubb/100EOS5D/small/{}'.format(name), res)

for file in glob.glob(path+'*.JPG'):
    dic.append(file)

if __name__ == "__main__":
    pool=Pool(14)
    pool.map(resizer, dic)
    pool.terminate()
