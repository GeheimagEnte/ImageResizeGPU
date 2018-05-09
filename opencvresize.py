#!/usr/bin/python
import argparse
import glob
import json
import time
from multiprocessing import Pool
from os import path, makedirs

import cv2 as cv
import piexif


def resizer(params):
    file = params['input']
    outFile = params['output']
    longside = params['longside']
    size = path.getsize(file)
    if size == 0:
        fileLog = 'File broken: {}'.format(file)
        print(fileLog)
        return '{}\n'.format(fileLog)
    img = cv.imread(file, cv.IMREAD_ANYCOLOR)
    height, width = img.shape[:2]
    dim = float(width) / float(height)
    if dim > 1:
        width = longside
        height = longside / dim
    else:
        width = longside * dim
        height = longside
    res = cv.resize(img, (int(width), int(height)), interpolation=params['interpolation'])
    cv.imwrite(outFile, res, [cv.IMWRITE_JPEG_QUALITY, params['quality']])
    exif_dict = piexif.load(file)
    if piexif.ImageIFD.Orientation in exif_dict["0th"]:
        exif_dict["0th"][piexif.ImageIFD.Orientation] = 0
        piexif.insert(piexif.dump(exif_dict), outFile)
    return ''


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resize all images in given Folder.",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("input", help="Input folder, i.e. originals folder.")
    parser.add_argument("output", help="Output folder, where the resized images are stored.")
    parser.add_argument("-t", "--threads", help="Number of concurrent resize threads. Default: 8", type=int, default=8)
    parser.add_argument("-l", "--longside", type=int, default=4000,
                        help="Number of pixels along the long side. The short side will be resized accordingly with the same factor. Default: 4000")
    parser.add_argument("-q", "--quality", help="JPEG image quality. Default: 90", type=int, default=90)
    parser.add_argument("-i", "--interpolation", choices=['0', '1', '2', '3', '4', '7'],
                        help="Interpolation method for resizing.\n0: Nearest - nearest neighbor interpolation\n1: "
                             "Linear - bilinear interpolation \n2: Cubic - bicubic interpolation\n3: Area - "
                             "resampling using pixel area relation. It may be a preferred method for image "
                             "decimation, as it gives moire'-free results.\n   But when the image is zoomed, "
                             "it is similar to the INTER_NEAREST method.\n4: Lanczos4 - Lanczos interpolation over "
                             "8x8 neighborhood\n7: Max - mask for interpolation codes\n"
                             "Default: 2: Cubic",
                        default=cv.INTER_CUBIC)
    args = parser.parse_args()

    if (not path.isdir(args.input)):
        print("Input path '{}' does not exist".format(args.input))
    else:
        if args.quality < 80:
            proceed = input("WARNING: Quality below 80%. Continue? [j,y/N]")
            if not proceed in ['j', 'J', 'y', 'Y']:
                raise SystemExit
        pool = Pool(args.threads)
        params = []
        inFiles = glob.glob(path.join(args.input, '**', '*.JPG'), recursive=True)
        for file in inFiles:
            outFile = path.join(args.output, path.relpath(file, start=args.input))
            if not path.isdir(path.dirname(outFile)):
                makedirs(path.dirname(outFile))
            params.append(dict(input=file, output=outFile, longside=args.longside, quality=args.quality,
                               interpolation=args.interpolation))
        start_time = time.time()
        log = pool.map(resizer, params)
        timeText = "--- %s seconds ---" % (time.time() - start_time)
        print(timeText)
        with open(path.join(args.output, 'resizeLog.txt'), 'w+') as logFile:
            logFile.write("Used parameters:\n{}\n\n".format(
                json.dumps(vars(args), sort_keys=False, indent=4, separators=(',', ': '))))
            logFile.write('{}\n'.format(timeText))
            logFile.writelines(log)
