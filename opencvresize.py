#!/usr/bin/python
import numpy as np
import cv2 as cv
import glob
from multiprocessing import Pool
import time
from piexif import transplant

path ='D:\\4711_TEST GPU\\4711_originale\\HERO\\'
dic = glob.glob(path+'*.JPG')
def resizer(file):
    name = file.split('\\')[-1]
    outFile = 'D:\\outputCVPy\\{}'.format(name)
    img = cv.imread(file, cv.IMREAD_IGNORE_ORIENTATION | cv.IMREAD_ANYCOLOR)
    height, width = img.shape[:2]
    dim = float(width)/float(height)
    if dim > 1:
        width=4000
        height= 4000/dim
    else:
        width=4000*dim
        height= 4000
    res = cv.resize(img, (int(width), int(height)), interpolation=cv.INTER_CUBIC)
    cv.imwrite(outFile, res, [cv.IMWRITE_JPEG_QUALITY, 80])
    transplant(file, outFile)

if __name__ == "__main__":
    pool=Pool(16)
    start_time = time.time()
    pool.map(resizer, dic)
    pool.terminate()
    print("--- %s seconds ---" % (time.time() - start_time))