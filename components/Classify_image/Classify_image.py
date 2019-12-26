import os
import sys
from os.path import isfile, join
from osgeo import ogr, osr
from zipfile import ZipFile
import subprocess

def main():
    # input image
    in_image = sys.argv[1]
    # model
    model = sys.argv[2]
    # classified image
    classified = sys.argv[3]

    # classify image
    classify_image(in_image, model, classified)


def classify_image(in_image, model, classified):

    # ensemble the extract sample pixel values system call
    sys_call = "otbcli_ImageClassifier -in "+in_image
    sys_call += " -model "+model
    sys_call += " -out "+classified
    os.system(sys_call)
    
main()