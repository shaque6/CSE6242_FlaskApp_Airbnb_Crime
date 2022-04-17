# CSE 6242 Airbnb / Crime Project

## Table of Contents

* [Environment Setup](#env)
* [Instructions](#instructions)

## Environment Setup

We found it was easiest to use Anaconda to install the appropiate packages because the fiona library was a challenge to install.

In Anaconda create a new environment and then run these commands in the Anaconda Prompt:

```bash
conda install -c conda-forge fiona=1.8.19
 
conda install -c conda-forge shapely rasterio pyproj pandas jupyterlab geopandas flask

pip install statsmodels
```

These packages are needed to work with Geopandas and using Flask as the framework for the website.

## Instructions

In the Anaconda prompt navigate to the folder with this repository and run

```bash
python app.py
```
and navigate to http://127.0.0.1:5000/ on your browser and the application will appear.