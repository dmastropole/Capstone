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

#from myfunctions import scrape_data

#latlon = (38.9097, -77.0443)

#df = scrape_data(latlon)
#df.to_csv('./src/data.csv')


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

