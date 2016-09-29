from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go
from datetime import datetime
import pandas as pd
import os

#for scraping 
from bs4 import BeautifulSoup
import requests
import re

#for saving data
import pickle

#pandas
import pandas as pd

#geocordinates
import geopy
import geopy.distance

#numpy
import numpy as np

#----------------- CREATE DATA FILE (DO ONCE) -----------------
#from myfunctions import scrape_data

#latlon = (38.9097, -77.0443)

#df = scrape_data(latlon)
#df.to_csv('./src/data.csv')

#------------------ TIMESERIES -------------------------------

df = pd.read_csv('data.csv')
#print df.head()

df['price'] = df['price'].str[1:].astype(int)
df_new = df[df['price'] <= 10000]
        
data = [go.Scatter(
            x=df_new['dtime'],
            y=df_new['price'],
            mode = 'markers')]

fig = go.Figure(data = data)
plot_url = plot(fig, filename="./templates/prices_timeseries.html", auto_open=False)

#------------------ HISTOGRAM --------------------------------
'''
df = pd.read_csv('data.csv')
prices = df['price'].tolist()
prices_vals = [float(x[1:]) for x in prices]

new_prices = []
for price in prices_vals:
    if price <= 10000:
        new_prices.append(price)

print max(new_prices)
print min(new_prices)
print len(new_prices)

data = [go.Histogram( x=new_prices, xbins=dict(
        start=0,
        end=10000,
        size=100
    ), )]

fig = go.Figure(data=data)
plot_url = plot(fig, filename="./templates/prices_histogram.html", auto_open=False)
'''
#------------------------- MAP -----------------------------------

'''
df_states = pd.read_csv('./src/states_regions.csv')
latlon = df_states['lat_lon'].tolist()

lon_list = []
lat_list = []
for ll in latlon:
    lat, lon = re.split(',',ll)
    lat = float(lat.strip("(").strip("'"))
    lon = float(lon.strip(" ").strip(")").strip("'"))
    
    lon_list.append(lon)
    lat_list.append(lat)
    
data = [ dict(
        type = 'scattergeo',
        locationmode = 'USA-states',
        lon = lon_list,
        lat = lat_list,
        text = df_states['region'],
        mode = 'markers',
        marker = dict( 
            size = 8, 
            opacity = 0.8,
            reversescale = True,
            autocolorscale = False,
            symbol = 'square',
            line = dict(
                width=1,
                color='rgba(102, 102, 102)'
            )
            
        ))]

layout = dict(
        title = 'Where are there listings?<br>(Hover for regional names)',
        geo = dict(
            scope='usa',
            projection=dict( type='albers usa' ),
            showland = True,
            landcolor = "rgb(250, 250, 250)",
            subunitcolor = "rgb(217, 217, 217)",
            countrycolor = "rgb(217, 217, 217)",
            countrywidth = 0.5,
            subunitwidth = 0.5        
        ),
    )

fig = dict( data=data, layout=layout )

plot_url = plot(fig, filename="./templates/region_map.html", auto_open=False)
#py.iplot( fig, validate=False, filename='d3-airports' )
'''
