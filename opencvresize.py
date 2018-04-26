#!/usr/bin/python
import numpy as np
import cv2 as cv
import glob


for file in glob.glob('/put/your/path/here/*.JPG'):
    print(file)
    img = cv.imread(file)
    height, width = img.shape[:2]
    res = cv.resize(img, ((int)(.5*width), (int)(.5*height)), interpolation=cv.INTER_CUBIC)
    name=file.split('\\')[-1]
    cv.imwrite('output/path/{}'.format(name), img)

