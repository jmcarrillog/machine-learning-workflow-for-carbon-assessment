## Semantic Workflows and Machine Learning for the Assessment of Carbon Storage by Urban Trees

This repository contains the data and source code of the [SciKnow'19](https://sciknow.github.io/sciknow2019/) paper titled *Semantic Workflows and Machine Learning for the Assessment of Carbon Storage by Urban Trees*, it also uncludes PDF documents of the paper and the slides.

The official proceedings are available in [CUWR](http://ceur-ws.org/Vol-2526/).

Authors: *Juan Carrillo <sup>1</sup>, Daniel Garijo <sup>2</sup>, Mark Crowley <sup>1</sup>, Rober Carrillo, Yolanda Gil <sup>2</sup>, Katherine Borda.*

* *<sup>1</sup> University of Waterloo. Canada*
* *<sup>2</sup> Information Sciences Institute. University of Southern California. USA*

### Abstract
> Climate science is critical for understanding both the causes and
consequences of changes in global temperatures and has become
imperative for decisive policy-making. However, climate science
studies commonly require addressing complex interoperability issues between data, software, and experimental approaches from
multiple fields. Scientific workflow systems provide unparalleled
advantages to address these issues, including reproducibility of
experiments, provenance capture, software reusability and knowledge sharing. In this paper, we introduce a novel workflow with
a series of connected components to perform spatial data preparation, classification of satellite imagery with machine learning
algorithms, and assessment of carbon stored by urban trees. To the
best of our knowledge, this is the first study that estimates carbon
storage for a region in Africa following the guidelines from the
Intergovernmental Panel on Climate Change (IPCC).

### Keywords
Reproducibility, scientific workflows, machine learning, land cover
mapping, carbon assessment, ESA Sentinel-2.

### Remark
We calculate that trees in the city of Juba remove 30,506 tonnes of Carbon per year, this amount is equivalent to the carbon dioxide emitted by 6632 passenger vehicles in the same period of time.

### Input data
* 4000 sample points distributed in four land categories: trees, grass, impervious, and water, with 1000 points
per category to have a balanced dataset. The points are digitized through visual inspection using Google Earth high resolution satellite imagery and stored as four individual KML files.
* Boundary of city of Juba in South Sudan retrieved in July 2019 from Open Street Maps.
* Sentinel-2 satellite image retrieved from the Copernicus Hub, clipped to the boundary of city of Juba to reduce the file size.

<img src="/readme-images/high-res-image.png" width="300" /><img src="/readme-images/mid-res-image.png" width="300" />

*Figure 1. Sample points and satellite imagery over the same location in Juba. Left: High resolution image from Google Earth. Right: Medium resolution Sentinel-2 image.*


### Workflow outputs
* Reports of model characteristics and classification accuracy for the Random Forests and Support Vector Machine pixel-based classifiers.
* Resulting land cover image for the city of Juba.

<img src="/readme-images/land-cover-map.png" width="300" />

*Figure 2. Land cover map for the city of Juba.*

### Software installation and setup

The semantic workflow from this paper implements multiple Extract Transform Load (ETL) operations over geospatial data using the GDAL Python bindings and also some Machine Learning image classification methods using the Orfeo Toolbox. We implement the steps in the workflow as independent components in the WINGS semantic workflow system. Below are the instructions to install and setup the required software to make use of our components.
1. Install [WINGS](https://wings-workflows.org/) using [Docker](https://www.docker.com/) by following the steps in this [guide](https://dgarijo.github.io/Materials/Tutorials/wings-docker/) authored by Daniel Garijo, Varun Ratnakar and Rajiv Mayani. For more information about [WINGS](https://wings-workflows.org/) including a and a thorough tutorial visit the official [WINGS](https://wings-workflows.org/) website. 
2. Run the WINGS Docker container and follow the next instructions within the container.
3. Install the GDAL python bindings. One alternative is to install [QGIS](https://qgis.org/) instead, which already comes with the GDAL Python bindings. The second alternative is to only install the GDAL Python bindings, preferably using [Conda](https://anaconda.org/conda-forge/gdal).
4. Install the Orfeo Toolbox by following the Linux section this [guide](https://www.orfeo-toolbox.org/CookBook/Installation.html).
5. Access the web interface from the Docker image at http://localhost:8080/wings-portal
6. Create a new Domain and upload the input datasets and components from this repository as shown in the examples of the WINGS [Tutorial](https://wings-workflows.org/tutorial/tutorial.html).
7. Create and run a workflow template following the same structure as seen in our complete workflow [image](/readme-images/complete_workflow.png).
8. Now you are ready to upload your own data and re-run the Carbon assessment workflow in other cities. :deciduous_tree::house_with_garden::deciduous_tree::school::deciduous_tree:

### Workflow components
Below is a brief summary of the functionality of each of the WINGS components we implemented, grouped in those dealing with geospatial vector data, raster data, and Machine Learning classification.
#### Components for processing geospatial vector data
* [AddField_to_Shapefile](/components/AddField_to_Shapefile). Takes a Shapefile packed into a single .zip file and creates a Shapefile field using a specified field name. Outputs a Shapefile packed into a single .zip file.
* [KML_to_Shapefile](/components/KML_to_Shapefile). Takes a KML file and converts it into a Shapefile with all of its related files (.shp .shx .dbf .prj) packed into a single .zip file.
* [Merge_Shapefiles](/components/Merge_Shapefiles). Takes multiple Shapefiles with the same characteristics (attributes and spatial coordinate reference system) and merges them into a single Shapefile packed into a .zip file.
* [Reproject_Shapefile](/components/Reproject_Shapefile). Takes a Shapefile packed into a single .zip file and reprojects it using a specified output spatial coordinate reference system. Outputs a Shapefile packed into a single .zip file.
* [SetField_in_Shapefile](/components/SetField_in_Shapefile). Takes a Shapefile packed into a single .zip file and sets an existing field to a specified value. Outputs a Shapefile packed into a single .zip file.
* [Split_Shp_by_perc](/components/Split_Shp_by_perc). Takes one Shapefile and splits it into two separate Shapefiles usign a split percentage. This component is useful for splitting a single Shapefile into separate training and validation sets.
#### Components for processing geospatial raster data
* [Clip_GeoTIFF](/components/Clip_GeoTIFF). Takes a GeoTIFF file, in our workflow a Sentinel-2 multispectral satellite image, and clips an area of interest defined by a Shapefile. Outputs the clipped GeoTIFF.
* [Extract_pixel_vals](/components/Extract_pixel_vals). Takes a GeoTIFF file and a Shapefile with sampling points and outputs the GeoTIFF pixel values for those sampling locations.
* [Image_visualization](/components/Image_visualization). Takes a GeoTIFF raw image with discrete pixel values and outputs a visualization ready image using a lookup table LUT of colors that it assigns to each pixel value.
* [Merge_Bands](/components/Merge_Bands). Takes multiple GeoTIFF images, each corresponding to one multispectral band, and merge them into one GeoTIFF image with multiple bands.
#### Components that implement Machine Learning for image classification
* [Classify_image](/components/Classify_image). Classifies an input multispectral satellite image using an already trained Machine Learning model also passed as input. Outputs a GeoTIFF file with discrete pixel values representing categories.
* [Evaluate_image_classification](/components/Evaluate_image_classification). Takes a satellite image already classified into land cover categories and a set of validation points and outputs an accuracy evaluation report.
* [Train_RF_Classifier](/components/Train_RF_Classifier). Takes a Shapefile with training points containing both multispectral values and their corresponding land cover category and trains a Random Forest classifier using specific parameters.
* [Train_SVM_Classifier](/components/Train_SVM_Classifier). Takes a Shapefile with training points containing both multispectral values and their corresponding land cover category and trains a Random Forest classifier using specific parameters.

### Acknowledgements


<img src="/readme-images/organizations.png" width="550" />

Juan Carrillo was financially supported for this project by the [Mitacs Globalink Research Award](https://www.mitacs.ca/en/programs/globalink) and the University of [Waterloo Machine Learning Lab](https://uwaterloo.ca/scholar/mcrowley/lab). Juan Carrillo gives special thanks to Mark Crowley, Daniel Garijo, and Yolanda Gil for their mentoring and contributions during this research project. Last but not least thanks to the administrative staff at Mitacs and the [Information Sciences Institute](https://www.isi.edu/) at University of Southern California for their kind help with multiple requirements.
