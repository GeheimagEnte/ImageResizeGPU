# ImageResizeGPU
##Usage 

    opencvresize.py [-h] [-t THREADS] [-l LONGSIDE] [-q QUALITY] [-i {0,1,2,3,4,7}] input output

Resize all images in given input Folder.

##Positional arguments
  input                 Input folder, i.e. originals folder.
  output                Output folder, where the resized images are stored.

##Optional arguments
1.  **-h, --help**
    : show this help message and exit
  
-   **-t THREADS, --threads THREADS**
    :                    Number of concurrent resize threads. Default: 8
                        
-   **-l LONGSIDE, --longside LONGSIDE**
    :                    Number of pixels along the long side. The short side will be resized accordingly with the same factor. Default: 4000
                        
-   **-q QUALITY, --quality QUALITY**
    :                    JPEG image quality. Default: 90
                        
-   **-i {0,1,2,3,4,7}, --interpolation {0,1,2,3,4,7}**
    :                    Interpolation method for resizing.
    - 0: Nearest - nearest neighbor interpolation
    - 1: Linear - bilinear interpolation
    - 2: Cubic - bicubic interpolation
    - 3: Area - resampling using pixel area relation. It may be a preferred method for image decimation, as it gives moire'-free results.
                           But when the image is zoomed, it is similar to the INTER_NEAREST method.
    - 4: Lanczos4 - Lanczos interpolation over 8x8 neighborhood
    - 7: Max - mask for interpolation codes
    
    Default: 2: Cubic
                        
                        
##Needed packages
- opencv-python
- piexif