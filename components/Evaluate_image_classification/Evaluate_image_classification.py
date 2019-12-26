import os
import sys
from os.path import isfile, join
from osgeo import ogr, osr
from zipfile import ZipFile
import subprocess

def main():
    # input land cover image
    land_cover = sys.argv[1]
    # input shapefile with validation samples
    val_file = sys.argv[2]
    # field name in shapefile that contains the label 
    field = sys.argv[3]
    # output report
    report = sys.argv[4]
    # output confusion matrix
    conf_matrix = sys.argv[5]

    # prepare input shapefile name
    val_shp = val_file[:-4]+'.shp'

    # unzip compressed files
    unzip_shapefile(val_file)

    # validate land cover classification
    evaluate_classification(land_cover, val_shp, field, report, conf_matrix)

    # clean folders from shapefile-related files other than zip files
    clean_folder(val_file)


def unzip_shapefile(in_file):
    with ZipFile(in_file, 'r') as zipObj:
        zipObj.extractall(os.path.dirname(in_file))


# function that removes all shapefile related files other than the zip file
def clean_folder(zip_file):
    # determine folder
    folder = os.path.dirname(zip_file)
    # pattern
    remove_pattern = os.path.basename(zip_file)[:-4]
    # list all files in folder
    all_files = [f for f in os.listdir(folder) if isfile(join(folder, f))]
    # remove the files
    for item in all_files:
        if remove_pattern in item and '.zip' not in item:
            os.remove(join(folder, item))


def evaluate_classification(land_cover, val_shp, field, report, conf_matrix):

    # prepare the system call
    otb_call = []
    otb_call.append('otbcli_ComputeConfusionMatrix')
    otb_call.append('-in')
    otb_call.append(land_cover)
    otb_call.append('-ref')
    otb_call.append('vector')
    otb_call.append('-ref.vector.in')
    otb_call.append(val_shp)
    otb_call.append('-ref.vector.field')
    otb_call.append(field)
    otb_call.append('-out')
    otb_call.append(conf_matrix)
    
    returned_string = subprocess.check_output(otb_call)

    with open(report, "wb") as f:
        f.write(returned_string)

main()