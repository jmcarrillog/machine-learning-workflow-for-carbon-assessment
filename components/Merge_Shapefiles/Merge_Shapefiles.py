import os
import sys
from osgeo import ogr, osr
from zipfile import ZipFile
from os.path import isfile, join


def main():
    # input shapefiles (zip file)
    in_files = []
    in_files.append(sys.argv[1])
    in_files.append(sys.argv[2])
    in_files.append(sys.argv[3])
    in_files.append(sys.argv[4])
    # output shapefile (zip file)
    out_file = sys.argv[5]

    # prepare input shapefiles names
    shp_names = []
    for file in in_files:
        shp_names.append(file[:-4]+'.shp')

    # prepare output shapefile name
    out_shapefile = out_file[:-4]+'.shp'

    # unzip compressed files
    for file in in_files:
        unzip_shapefile(file)

    # set driver
    driver = ogr.GetDriverByName('ESRI Shapefile')

    # call merge shapefiles function
    merge_shapefiles(shp_names, out_shapefile, driver)

    # zip the output shapefile
    zip_shapefile(out_file)

    # clean input and output folders from shapefile-related files other than zip files
    for file in in_files:
        clean_folder(file)
    clean_folder(out_file)


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


def merge_shapefiles(shp_names, out_shapefile, driver):

    # get the input datsets and layers
    in_datasets = []
    for shp in shp_names:
        in_datasets.append(driver.Open(shp))
    
    in_layers = []
    for i_data in in_datasets:
        in_layers.append(i_data.GetLayer()) 

    # create the output layer
    if os.path.exists(out_shapefile):
        driver.DeleteDataSource(out_shapefile)
    outDataSet = driver.CreateDataSource(out_shapefile)
    # use geometry definition from the first input layer
    outLayer = outDataSet.CreateLayer(out_shapefile[:-4], geom_type=in_layers[0].GetGeomType())

    # use layer and fields definition from the first input layer
    inLayerDefn = in_layers[0].GetLayerDefn()
    for i in range(0, inLayerDefn.GetFieldCount()):
        fieldDefn = inLayerDefn.GetFieldDefn(i)
        outLayer.CreateField(fieldDefn)

    # get the output layer's feature definition
    outLayerDefn = outLayer.GetLayerDefn()

    # loop through the input layers 
    for lyr in in_layers:
        # loop through the input features
        inFeature = lyr.GetNextFeature()
        while inFeature:
            # get the input geometry
            geom = inFeature.GetGeometryRef()
            # create a new feature
            outFeature = ogr.Feature(outLayerDefn)
            # set the geometry
            outFeature.SetGeometry(geom)
            # set all attributes with the same value of input layers
            for i in range(0, outLayerDefn.GetFieldCount()):
                outFeature.SetField(outLayerDefn.GetFieldDefn(i).GetNameRef(), inFeature.GetField(i))
            # add the feature
            outLayer.CreateFeature(outFeature)
            # dereference the features and get the next input feature
            outFeature = None
            inFeature = lyr.GetNextFeature()

    # use same SpatialReference from first input layer
    outSpatialRef = in_layers[0].GetSpatialRef()
    
    # export .prj file
    outSpatialRef.MorphToESRI()
    prjfile = open(out_shapefile[:-4]+'.prj', 'w')
    prjfile.write(outSpatialRef.ExportToWkt())
    prjfile.close()

    # remove references to datasets
    for i in range(len(in_datasets)):
        in_datasets[i] = None
    outDataSet = None


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
