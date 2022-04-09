from flask import Flask, render_template, url_for, request

import pandas as pd
import matplotlib.pyplot as plt
import descartes
import geopandas as gpd
import numpy as np
from shapely.geometry import Point, Polygon
import folium
import branca

from MapScripts.createChicagoMap import createChicagoMap
from MapScripts.createBostonMap import createBostonMap


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
    price = output["price"]
    
    if name == 'Boston':
        createBostonMap(price)

    if name == 'Chicago':
        createChicagoMap(price)

    return render_template('index.html', name = name, price=price)
    




if __name__ == "__main__":
    app.run(debug=True)