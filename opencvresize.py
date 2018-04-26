#!/usr/bin/python
import numpy as np
import cv2 as cv
import glob


for file in glob.glob('/home/evilblubb/100EOS5D/*.JPG'):
    img = cv.UMat(cv.imread(file))
    res = cv.resize(img,None, fx =0.5, fy=0.5, interpolation=cv.INTER_CUBIC)
    name=file.split('/')[-1]
    print(name)
    cv.imwrite('/home/evilblubb/100EOS5D/small/{}'.format(name), res)

