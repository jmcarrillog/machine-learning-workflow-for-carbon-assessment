import os
import sys
from os.path import isfile, join
from osgeo import ogr, osr
from zipfile import ZipFile
import subprocess

def main():
    # input image
    image = sys.argv[1]
    # input training samples
    train_file = sys.argv[2]
    # class field in training samples
    field = sys.argv[3]
    # output training samples with pixel values
    train_file_pixval = sys.argv[4]

    # prepare input shapefile name
    in_shp = train_file[:-4]+'.shp'
    # prepare output shapefile name
    out_shp = train_file_pixval[:-4]+'.shp'

    # unzip compressed file
    unzip_shapefile(train_file)

    # call extract pixel values function
    extr_pix_val(image, in_shp, field, out_shp)

    # zip the output shapefile
    zip_shapefile(train_file_pixval)

    # clean folders from shapefile-related files other than zip files
    clean_folder(train_file)
    clean_folder(train_file_pixval)


def unzip_shapefile(in_file):
    with ZipFile(in_file, 'r') as zipObj:
        zipObj.extractall(os.path.dirname(in_file))

def zip_shapefile(out_file):
    # determine output folder
    output_folder = os.path.dirname(out_file)
    # list all files in output folder
    all_files = [f for f in os.listdir(output_folder) if isfile(join(output_folder, f))]
    # create the zip file
    zip_file = ZipFile(out_file, 'w')
    # common name for all shapefile related output files
    common_name = os.path.basename(out_file)[:-4]
    # filter files corresponding to the output shapefile
    for item in all_files:
        if common_name in item:
            zip_file.write(join(output_folder, item), arcname=item)
    zip_file.close()

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


def copy_shp(in_shapefile, out_shapefile):
    # set driver
    driver = ogr.GetDriverByName('ESRI Shapefile')
    
    # get the input layer
    inDataSet = driver.Open(in_shapefile)
    inLayer = inDataSet.GetLayer()

    # create the output layer
    if os.path.exists(out_shapefile):
        driver.DeleteDataSource(out_shapefile)
    outDataSet = driver.CreateDataSource(out_shapefile)
    outLayer = outDataSet.CreateLayer(out_shapefile[:-4], geom_type=inLayer.GetGeomType())

    # add input shapefile fields
    inLayerDefn = inLayer.GetLayerDefn()
    for i in range(0, inLayerDefn.GetFieldCount()):
        fieldDefn = inLayerDefn.GetFieldDefn(i)
        outLayer.CreateField(fieldDefn)

    # get the output layer's feature definition
    outLayerDefn = outLayer.GetLayerDefn()

    # loop through the input features
    inFeature = inLayer.GetNextFeature()
    while inFeature:
        # get the input geometry
        geom = inFeature.GetGeometryRef()
        # create a new feature
        outFeature = ogr.Feature(outLayerDefn)
        # set the geometry
        outFeature.SetGeometry(geom)
        # set the attributes
        for i in range(0, outLayerDefn.GetFieldCount()):
            outFeature.SetField(outLayerDefn.GetFieldDefn(i).GetNameRef(), inFeature.GetField(i))
        # add the feature
        outLayer.CreateFeature(outFeature)
        # dereference the features and get the next input feature
        outFeature = None
        inFeature = inLayer.GetNextFeature()

    # same SpatialReference
    outSpatialRef = inLayer.GetSpatialRef()
    
    # export .prj file
    outSpatialRef.MorphToESRI()
    prjfile = open(out_shapefile[:-4]+'.prj', 'w')
    prjfile.write(outSpatialRef.ExportToWkt())
    prjfile.close()

    # remove references to datasets
    inDataSet = None
    outDataSet = None

def init_otb():
    os.system(". /usr/local/otb/OTB-6.6.1-Linux64/otbenv.profile")

def extr_pix_val(image, in_shp, field, out_shp):

    # initialize orfeo toolbox command line tools
    init_otb()
    
    # copy input shp into out shape
    copy_shp(in_shp, out_shp)

    # ensemble the extract sample pixel values system call
    sys_call = "otbcli_SampleExtraction -in "+image+" -vec "
    sys_call += in_shp+" -outfield prefix -outfield.prefix.name band_ "
    sys_call += " -field "+field+" -out "+out_shp
    
    os.system(sys_call)
    
main()