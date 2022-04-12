import pandas as pd
import matplotlib.pyplot as plt
import descartes
import geopandas as gpd
import numpy as np
from shapely.geometry import Point, Polygon
import folium
import branca
from static.popup_html import popup_html # code used to show features when clicking airbnb


def createMap(path_choro, path_listing, abrv, price=200):

    map_and_stats_2 = gpd.read_file(path_choro)
    # community_map = community_map.rename(columns={'name':'community'})

    # Commenting out this section and saving file directly
    # crime data taken from https://data.lacity.org/Public-Safety/Crime-Data-from-2020-to-Present/2nrs-mtv8/data
    # df = pd.read_csv('./Data/LA_Crimes.csv')
    # crs = {'init' : 'epsg:4326'}
    # df = df.dropna(subset=['LATITUDE'])
    # df= df[df['LATITUDE'] != 0]

    # geometry = [Point(xy) for xy in zip(df["LONGITUDE"], df["LATITUDE"])]
    # geometry[:3]


    # geo_df = gpd.GeoDataFrame(df, crs = crs, geometry = geometry) 


    # # taken from https://towardsdatascience.com/tagging-a-location-to-a-shapefile-area-using-geopandas-5d74336128bf
    # geo_df['community'] = ''
    # for idx in range(community_map.shape[0]):
    #     #For every lat/long, find if they reside within a community
    #     pip = geo_df.within(community_map.loc[idx, 'geometry'])
    #     if pip.sum() > 0:
    #         geo_df.loc[pip, 'community']  = community_map.loc[idx, 'community']
    # geo_df.to_file("LA_SHP\Summarized_Shp\LACrime.shp")

    #### Groupby analysis is done in Jupyter notebook then saved as .shp file
    # geo_df = gpd.read_file("SHP\LA_SHP\Summarized_Shp\LACrime.shp")
    #
    # # taking group by and then reverting back to data frame to use
    # # https://technology.amis.nl/data-analytics/convert-groupby-result-on-pandas-data-frame-into-a-data-frame-using-to_frame/
    # crimebycommunity = geo_df.groupby(['community'])['community'].count().to_frame(name = 'count').reset_index()
    #
    #
    # crimebycommunity['community'].replace('', np.nan, inplace=True)
    # crimebycommunity = crimebycommunity.dropna(subset=['community'])
    #
    #
    # map_and_stats = community_map.merge(crimebycommunity, on="community")

    # map_and_stats_2 = map_and_stats[['community','geometry','count']]

    # # Trying Folium for Interactivity


    # https://vverde.github.io/blob/interactivechoropleth.html

    x_map = map_and_stats_2.centroid.x.mean()
    y_map = map_and_stats_2.centroid.y.mean()



    mymap = folium.Map(location=[y_map, x_map], zoom_start=11,tiles=None)
    folium.TileLayer('CartoDB positron',name="Light Map",control=False).add_to(mymap)


    myscale = (map_and_stats_2['count'].quantile((0,0.5,0.9,1))).tolist()


    mymap.choropleth(
        geo_data=map_and_stats_2,
        name='Choropleth',
        data=map_and_stats_2,
        columns=['community','count'],
        key_on="feature.properties.community",
        fill_color='Reds', #https://matplotlib.org/3.5.1/tutorials/colors/colormaps.html          sequential color maps
        threshold_scale=myscale,
        fill_opacity=0.5,
        line_opacity=0.2,
        legend_name='Crime Count',
        smooth_factor=0
    )

    style_function = lambda x: {'fillColor': '#ffffff',
                                'color':'#000000',
                                'fillOpacity': 0.1,
                                'weight': 0.1}

    highlight_function = lambda x: {'fillColor': '#000000',
                                    'color':'#000000',
                                    'fillOpacity': 0.50,
                                    'weight': 0.1}

    CrimeCount = folium.features.GeoJson(
        map_and_stats_2,
        style_function=style_function,
        control=False,
        highlight_function=highlight_function,
        tooltip=folium.features.GeoJsonTooltip(
            fields=['community','count'],
            aliases=['Neighborhood: ','Count of Crimes '],
            style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
        )
    )
    mymap.add_child(CrimeCount)
    mymap.keep_in_front(CrimeCount)
    folium.LayerControl().add_to(mymap)

    df_airbnb = pd.read_csv(path_listing)


    airbnb_locations = df_airbnb[['latitude','longitude']]
    airbnb_list = airbnb_locations.values.tolist()

    price = int(price)
    df_airbnb_price_filtered = df_airbnb[df_airbnb.price==price]
    rows = len(df_airbnb_price_filtered)
    #https://georgetsilva.github.io/posts/mapping-points-with-folium/
    #https://towardsdatascience.com/folium-map-how-to-create-a-table-style-pop-up-with-html-code-76903706b88a
    for point in range(0,rows):
        i = point
        html = popup_html(i,df_airbnb_price_filtered)
        iframe = branca.element.IFrame(html=html,width=200,height=200)
        popup = folium.Popup(folium.Html(html, script=True), max_width=500)
        folium.Marker(airbnb_list[point], popup).add_to(mymap)

    mymap.save("./static/index_" + abrv + ".html")


if __name__ == "__main__":
    createMap()