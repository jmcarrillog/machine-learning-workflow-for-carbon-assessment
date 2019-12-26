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
    # input shapefile with validation pixel samples
    val_file_pixval = sys.argv[3]

    # SVM specific parameters
    # image statistics
    img_stats = sys.argv[4]
    # kernel type
    kernel_type = sys.argv[5]

    # output model
    out_model = sys.argv[6]

    # output report
    out_rep = sys.argv[7]

    # prepare input shapefiles name
    train_shp = train_file_pixval[:-4]+'.shp'
    val_shp = val_file_pixval[:-4]+'.shp'

    # unzip compressed files
    unzip_shapefile(train_file_pixval)
    unzip_shapefile(val_file_pixval)

    # create and train model
    train_svm_model(train_shp, field, val_shp, img_stats, kernel_type, out_model, out_rep)

    # clean folders from shapefile-related files other than zip files
    clean_folder(train_file_pixval)
    clean_folder(val_file_pixval)


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


def init_otb():
    # locate Orfeo env variables initialization script
    otb_ini_file = subprocess.run(['locate', '-e', 'otbenv.profile', '-n', '1'], stdout=subprocess.PIPE)
    # remove carriage return
    otb_ini_file = otb_ini_file.stdout.decode('utf-8')[:-1]
    # initialize OTB command line tools
    os.system('. '+otb_ini_file)
    #sys_reply = subprocess.run(['.',otb_ini_file], stdout=subprocess.PIPE)
    #print(sys_reply)


def train_svm_model(train_shp, field, val_shp, img_stats, kernel_type, out_model, out_rep):

    # initialize otb
    init_otb()

    otb_train_call = []
    otb_train_call.append('otbcli_TrainVectorClassifier')
    otb_train_call.append('-io.vd')
    otb_train_call.append(train_shp)
    otb_train_call.append('-cfield')
    otb_train_call.append(field)
    otb_train_call.append('-valid.vd')
    otb_train_call.append(val_shp)

    otb_train_call.append('-io.stats')
    otb_train_call.append(img_stats)

    otb_train_call.append('-classifier')
    otb_train_call.append('libsvm')

    otb_train_call.append('-classifier.libsvm.m')
    otb_train_call.append('csvc')

    otb_train_call.append('-classifier.libsvm.k')
    otb_train_call.append(kernel_type)

    otb_train_call.append('-classifier.libsvm.opt')
    otb_train_call.append('true')

    otb_train_call.append('-io.out')
    otb_train_call.append(out_model)
    otb_train_call.append('-feat')
    otb_train_call.append('band_0')
    otb_train_call.append('band_1')
    otb_train_call.append('band_2')
    otb_train_call.append('band_3')

    with open(out_rep, "w") as f:
        subprocess.run(otb_train_call, stdout=f)

    
    
main()