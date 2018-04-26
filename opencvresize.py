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

    dim = float(width)/float(height)
    if dim > 1:
        width=4000
        height= 4000/dim
        start_time = time.time()
        res = cv.resize(img, (int(width), int(height)), interpolation=cv.INTER_CUBIC)
        print("--- %s seconds ---" % (time.time() - start_time))
    else:
        width=4000*dim
        height= 4000
        start_time = time.time()
        res = cv.resize(img, (int(width), int(height)), interpolation=cv.INTER_CUBIC)
        print("--- %s seconds ---" % (time.time() - start_time))
    name=file.split('/')[-1]
    cv.imwrite('/home/evilblubb/100EOS5D/small/{}'.format(name), res)

for file in glob.glob(path+'*.JPG'):
    dic.append(file)

if __name__ == "__main__":
    pool=Pool(16)
    pool.map(resizer, dic)
    pool.terminate()
