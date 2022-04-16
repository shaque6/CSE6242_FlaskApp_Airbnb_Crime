from flask import Flask, render_template, url_for, request

import pandas as pd
import matplotlib.pyplot as plt
import descartes
import geopandas as gpd
import numpy as np
from shapely.geometry import Point, Polygon
import folium
import branca
import math

# from MapScripts.createChicagoMap import createChicagoMap
# from MapScripts.createBostonMap import createBostonMap
# from MapScripts.createLAMap import createLAMap
from MapScripts.createMap import createMap
from static.RegressionFXN import get_price



app = Flask(__name__)

 

@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")



@app.route('/map',methods=['POST', 'GET'])
def result():
    output = request.form.to_dict()
    print(output)
    name = output["name"]
    RoomType = output["RoomType"]
    accommodate = float(output["accommodate"])
    bed = float(output["bed"])
    bathroom = float(output["bathroom"])
    neighborhood = output["neighborhood"]
    price = round(get_price(name, RoomType, accommodate, bathroom, bed, neighborhood),2)
    price_lower = round(price-2.5)
    price_upper = round(price+2.5)
    print(price_lower, price_upper)
    path_choro = ''
    path_listing = ''
    
    if name == 'Boston':
        path_choro = './SHP/Boston_SHP/Summarized_Shp/BostonCrime.shp'
        path_listing = './Data/Boston_listings.csv'
        abrv = 'Boston'

    if name == 'Chicago':
        path_choro = './SHP/Chicago_SHP/Summarized_Shp/ChicagoCrime.shp'
        path_listing = './Data/Chicago_listings.csv'
        abrv = 'Chicago'

    if name == 'Los Angeles':
        path_choro = './SHP/LA_SHP/Summarized_SHP/LACrime.shp'
        path_listing = './Data/LA_listings.csv'
        abrv = 'LA'

    if name == 'San Francisco':
        path_choro = './SHP/SF_SHP/Summarized_SHP/SFCrime.shp'
        path_listing = './Data/SF_listings.csv'
        abrv = "SF"

    if name == 'New York City':
        path_choro = './SHP/NYC_SHP/Summarized_Shp/NYCCrime.shp'
        path_listing = './Data/NYC_listings.csv'
        abrv = "NYC"

    createMap(path_choro, path_listing, abrv, price)

    return render_template('index.html', name = name, price=price, price_lower = price_lower, price_upper = price_upper, RoomType = RoomType, accommodate=int(accommodate), bed=int(bed), bathroom=bathroom, neighborhood=neighborhood)


if __name__ == "__main__":
    app.run(debug=True)