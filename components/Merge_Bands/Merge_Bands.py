import os
import sys
from os.path import isfile, join
import subprocess

def main():
    # input band 1
    band_1 = sys.argv[1]
    # input band 2
    band_2 = sys.argv[2]
    # input band 3
    band_3 = sys.argv[3]
    # input band 4
    band_4 = sys.argv[4]
    # output GeoTIFF image
    output_image = sys.argv[5]

    # call merge function
    merge_bands(band_1, band_2, band_3, band_4, output_image)

def merge_bands(band_1, band_2, band_3, band_4, output_image):

    # ensemble the system call
    sys_call = "python /usr/bin/gdal_merge.py -separate -ot UInt16 -of GTiff -o "
    sys_call += output_image+" "+band_1+" "+band_2+" "+band_3+" "+band_4
    
    os.system(sys_call)

main()