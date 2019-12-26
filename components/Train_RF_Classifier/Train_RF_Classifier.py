import os
import sys
from os.path import isfile, join
from osgeo import ogr, osr
from zipfile import ZipFile
import subprocess

def main():
    # input shapefile with training pixel samples
    train_file_pixval = sys.argv[1]

    # class field in training samples
    field = sys.argv[2]
    # Random Forest specific parameters
    # number of trees in the forest
    num_trees = sys.argv[3]
    # maximum depth of the tree
    max_depth = sys.argv[4]
    # minimum number of samples in each node
    min_per_node = sys.argv[5]
    # output model
    out_model = sys.argv[6]

    # prepare input shapefiles name
    train_shp = train_file_pixval[:-4]+'.shp'

    # unzip compressed files
    unzip_shapefile(train_file_pixval)

    # create and train model
    train_rf_model(train_shp, field, num_trees, max_depth, min_per_node, out_model)

    # clean folders from shapefile-related files other than zip files
    clean_folder(train_file_pixval)


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


def train_rf_model(train_shp, field, num_trees, max_depth, min_per_node, out_model):

    # prepare the system call
    otb_train_call = 'otbcli_TrainVectorClassifier -io.vd '+train_shp+' -cfield '+field
    otb_train_call += ' -classifier rf -classifier.rf.nbtrees '+num_trees
    otb_train_call += ' -classifier.rf.max '+max_depth+' -classifier.rf.min '+min_per_node
    otb_train_call += ' -io.out '+out_model
    otb_train_call += ' -feat band_0 band_1 band_2 band_3'

    os.system(otb_train_call)

main()