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

### Input data
* 4000 sample points distributed in four land categories: trees, grass, impervious, and water, with 1000 points
per category to have a balanced dataset. The points are digitized through visual inspection using Google Earth high resolution satellite imagery and stored as four individual KML files.
* Boundary of city of Juba in South Sudan retrieved in July 2019 from Open Street Maps.
* Sentinel-2 satellite image retrieved from the Copernicus Hub, clipped to the boundary of city of Juba to reduce the file size.

### Workflow outputs
* Reports of model characteristics and classification accuracy for the Random Forests and Support Vector Machine pixel-based classifiers.
* Resulting land cover map for the city of Juba.

### Software installation and setup

The semantic workflow from this paper implements multiple Extract Transform Load (ETL) operations over geospatial data using the GDAL Python bindings and also some Machine Learning image classification methods using the Orfeo Toolbox. We implement the steps in the workflow as independent components in the WINGS semantic workflow system. Below are the instructions to install and setup the required software to make use of our components.
1. Install [WINGS](https://wings-workflows.org/) using [Docker](https://www.docker.com/) by following the steps in this [guide](https://dgarijo.github.io/Materials/Tutorials/wings-docker/) authored by Daniel Garijo, Varun Ratnakar and Rajiv Mayani. For more information about [WINGS](https://wings-workflows.org/) including a and a thorough tutorial visit the official [WINGS](https://wings-workflows.org/) website. 
2. Run the WINGS Docker container and follow the next instructions within the container.
3. Install the GDAL python bindings. One alternative is to install [QGIS](https://qgis.org/) instead, which already comes with the GDAL Python bindings. The second alternative is to only install the GDAL Python bindings, preferably using [Conda](https://anaconda.org/conda-forge/gdal).
4. Install the Orfeo Toolbox by following the Linux section this [guide](https://www.orfeo-toolbox.org/CookBook/Installation.html).
5. Access the web interface from the Docker image at http://localhost:8080/wings-portal
6. Create a new Domain and upload the input datasets and components as shown in the examples of the WINGS [Tutorial](https://wings-workflows.org/tutorial/tutorial.html).
7. Now you are ready to upload your own data and re-run the Carbon assessment workflow in other cities. :deciduous_tree::house_with_garden::deciduous_tree::school::deciduous_tree:

### Workflow components
Below is a brief summary of the functionality of each of the WINGS components we implemented, grouped in those dealing with geospatial vector data, raster data, and Machine Learning classification.



