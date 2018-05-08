#!/usr/bin/python
from os import path, makedirs
import cv2 as cv
import glob
from multiprocessing import Pool
import time
import argparse
import piexif

def resizer(params):
    file = params['input']
    outFile = params['output']
    longside = params['longside']
    img = cv.imread(file, cv.IMREAD_ANYCOLOR)
    height, width = img.shape[:2]
    dim = float(width) / float(height)
    if dim > 1:
        width = longside
        height = longside / dim
    else:
        width = longside * dim
        height = longside
    res = cv.resize(img, (int(width), int(height)), interpolation=cv.INTER_CUBIC)
    cv.imwrite(outFile, res, [cv.IMWRITE_JPEG_QUALITY, params['quality']])
    exif_dict = piexif.load(file)
    if piexif.ImageIFD.Orientation in exif_dict["0th"]:
        exif_dict["0th"][piexif.ImageIFD.Orientation] = 0
        piexif.insert(piexif.dump(exif_dict), outFile)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resize all images in given Folder.")
    parser.add_argument("input", help="Input folder, i.e. originals folder.")
    parser.add_argument("output", help="Output folder, where the resized images are stored.")
    parser.add_argument("-t", "--threads", help="Number of concurrent resize threads. Default: 8", type=int, default=8)
    parser.add_argument("-l", "--longside", type=int, default=4000,
                        help="Number of pixels along the long side. The short side will be resized accordingly with the same factor. Default: 4000")
    parser.add_argument("-q", "--quality", help="JPEG image quality. Default: 90", type=int, default=90)
    args = parser.parse_args()

    if (not path.isdir(args.input)):
        print("Input path '{}' does not exist".format(args.input))
    else:
        pool = Pool(args.threads)
        params = []
        inFiles = glob.glob(path.join(args.input, '**', '*.JPG'), recursive=True)
        for file in inFiles:
            outFile = path.join(args.output, path.relpath(file, start=args.input))
            if (not path.isdir(path.dirname(outFile))):
                makedirs(path.dirname(outFile))
            params.append(dict(input=file, output=outFile, longside=args.longside, quality=args.quality))
        start_time = time.time()
        pool.map(resizer, params)
        pool.terminate()
        print("--- %s seconds ---" % (time.time() - start_time))
