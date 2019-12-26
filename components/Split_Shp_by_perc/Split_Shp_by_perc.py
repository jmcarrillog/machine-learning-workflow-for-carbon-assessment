import os
import sys
import random
from osgeo import ogr, osr
from zipfile import ZipFile
from os.path import isfile, join


def main():
    # input (zip file)
    in_file = sys.argv[1]
    # split percentage in the interval (0, 1)
    split_perc = float(sys.argv[2])
    # output shp 1 with split_perc number of samples (zip file)
    out_file_1 = sys.argv[3]
    # output shp 2 with 1 - split_perc number of samples (zip file)
    out_file_2 = sys.argv[4]

    # prepare input shapefile name
    in_shp = in_file[:-4]+'.shp'
    # prepare output shapefiles names
    out_shp_1 = out_file_1[:-4]+'.shp'
    out_shp_2 = out_file_2[:-4]+'.shp'
    
    # unzip compressed file
    unzip_shapefile(in_file)

    # call split shapefiles
    split_shp_by_perc(in_shp, split_perc, out_shp_1, out_shp_2)

    # zip the output shapefile
    zip_shapefile(out_file_1)
    zip_shapefile(out_file_2)

    # clean input and output folders from shapefile-related files other than zip files
    clean_folder(in_file)
    clean_folder(out_file_1)
    clean_folder(out_file_2)


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

def get_feature_ids(inLayer):
    feat_ids = []
    # loop through the input features
    inFeature = inLayer.GetNextFeature()
    while inFeature:
        # append feature value
        feat_ids.append(inFeature.GetFID())
        inFeature = inLayer.GetNextFeature()
    return feat_ids

def split_shp_by_perc(in_shp, split_perc, out_shp_1, out_shp_2):

    # set driver
    driver = ogr.GetDriverByName('ESRI Shapefile')

    # get the input layer
    inDataSet = driver.Open(in_shp)
    inLayer = inDataSet.GetLayer()

    # create the output layers
    if os.path.exists(out_shp_1):
        driver.DeleteDataSource(out_shp_1)
    outDataSet_1 = driver.CreateDataSource(out_shp_1)
    outLayer_1 = outDataSet_1.CreateLayer(out_shp_1[:-4], geom_type=inLayer.GetGeomType())
    if os.path.exists(out_shp_2):
        driver.DeleteDataSource(out_shp_2)
    outDataSet_2 = driver.CreateDataSource(out_shp_2)
    outLayer_2 = outDataSet_2.CreateLayer(out_shp_2[:-4], geom_type=inLayer.GetGeomType())

    # add output shapefiles fields
    inLayerDefn = inLayer.GetLayerDefn()
    for i in range(0, inLayerDefn.GetFieldCount()):
        fieldDefn = inLayerDefn.GetFieldDefn(i)
        outLayer_1.CreateField(fieldDefn)
        outLayer_2.CreateField(fieldDefn)

    # input and output layers definition are the same
    outLayerDefn = inLayerDefn

    # get input layer feature count
    in_lyr_cnt = inLayer.GetFeatureCount()

    # obtain a shuffled list of input feature ids
    feat_ids = get_feature_ids(inLayer)
    random.shuffle(feat_ids)

    # track number of features in first output layer
    cnt_first_layer = 0
    
    # fill first output layer with split_perc percentage of features
    while len(feat_ids) > 0:
        # loop over all features
        f_id = feat_ids.pop()
        inFeature = inLayer.GetFeature(f_id)
        # get the input geometry
        geom = inFeature.GetGeometryRef()
        # create a new feature
        outFeature = ogr.Feature(outLayerDefn)
        # set the geometry
        outFeature.SetGeometry(geom)
        # set all attributes
        for i in range(0, outLayerDefn.GetFieldCount()):
            outFeature.SetField(outLayerDefn.GetFieldDefn(i).GetNameRef(), inFeature.GetField(i))

        # check if first layer is full
        if cnt_first_layer < int(in_lyr_cnt*(split_perc)):
            # add the feature
            outLayer_1.CreateFeature(outFeature)
            cnt_first_layer += 1
        else:
            outLayer_2.CreateFeature(outFeature)
        # dereference the features and get the next input feature
        outFeature = None

    # same SpatialReference
    outSpatialRef = inLayer.GetSpatialRef()
    
    # export .prj file
    outSpatialRef.MorphToESRI()
    prjfile = open(out_shp_1[:-4]+'.prj', 'w')
    prjfile.write(outSpatialRef.ExportToWkt())
    prjfile.close()
    prjfile = open(out_shp_2[:-4]+'.prj', 'w')
    prjfile.write(outSpatialRef.ExportToWkt())
    prjfile.close()
    # remove references to datasets
    inDataSet = None
    outDataSet_1 = None
    outDataSet_2 = None


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


main()
