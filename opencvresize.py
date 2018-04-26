#!/usr/bin/python
import numpy as np
import cv2 as cv
import glob
from multiprocessing import Pool
import time

path ='/home/evilblubb/100EOS5D/'
dic=[]
def resizer(file):
    img = cv.imread(file)
    height, width = img.shape[:2]
    UMatimg=cv.UMat(img)
    dim = float(width)/float(height)
    if dim > 1:
        width=4000
        height= 4000/dim
        res = cv.resize(UMatimg, (int(width), int(height)), interpolation=cv.INTER_CUBIC)
    else:
        width=4000*dim
        height= 4000
        res = cv.resize(UMatimg, (int(width), int(height)), interpolation=cv.INTER_CUBIC)
    name=file.split('/')[-1]
    cv.imwrite('/home/evilblubb/100EOS5D/small/{}'.format(name), res)

for file in glob.glob(path+'*.JPG'):
    dic.append(file)

if __name__ == "__main__":
    start_time = time.time()
    pool=Pool(16)
    pool.map(resizer, dic)
    pool.terminate()
    print("--- %s seconds ---" % (time.time() - start_time))
