from flask import Flask, render_template, request, redirect
import requests
import simplejson as json
import re
import pickle

import numpy as np
import scipy.special
import pandas as pd

from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go

import geopy
import geopy.distance
from datetime import datetime
import os

import myfunctions
#import build_model

#machine learning
import sklearn as sk
from sklearn.base import BaseEstimator, RegressorMixin 
from sklearn import neighbors
from sklearn import ensemble, feature_extraction
from sklearn.grid_search import GridSearchCV
from sklearn import neighbors, cross_validation, grid_search, linear_model
from sklearn.linear_model import LinearRegression, LassoCV
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction import DictVectorizer
from sklearn import pipeline
from sklearn.preprocessing import Imputer

#--------------------------------------------------------------------

class categoryTransformer(sk.base.BaseEstimator, sk.base.TransformerMixin):

    def __init__(self, colname):
        self.colname = colname
        pass
        
    def fit(self, X, y=None):
        return self

    def transform(self, X):      
        self.val = X[self.colname]        
        return self.val

#--------------------------------------------------------------------

app = Flask(__name__)


@app.route('/')
def main():
  return render_template('index.html')

@app.route('/about_tool')
def about_tool():
  return render_template('about_tool.html')
  
@app.route('/tool', methods=['GET','POST'])
def tool():
  if request.method == 'GET':
    return render_template('tool.html')
  else:
    return redirect('/results')

@app.route('/results', methods=['GET', 'POST'])
def get_data():
    address = request.form['address']
    bdrms = request.form['bdrms']
    baths = request.form['baths']
    sqfootage = request.form['sqfootage']
    
    if not address or not bdrms or not baths or not sqfootage:
        return render_template('error_page.html', message='Please fill in all of the fields.')
    
    #Get lat and lon from address
    address = '+'.join(address.split())
    api_key = '&key=AIzaSyCyYqXfiJLjQwRSS9PvKpWvfvnxP0A6Sw0'
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json?address='
    full_url = base_url + address + api_key
    r = requests.get(full_url)
    geo_data = r.content
    if len(geo_data) == 52:
        return render_template('error_page.html', message="Your address doesn't seem to exist.")
    latlon = re.findall(r'"location"\s+:\s+{\s+"lat"\s+:\s+(.*),\s+"lng"\s+:\s+(.*)\s+}', geo_data)
    lat = float(latlon[0][0].strip("'"))
    lng = float(latlon[0][1].strip("'"))
    
    
    #make sure that address is within 100 km of DC center (capitol)
    lat_cap = 38.89
    lng_cap = -77.01
    dist = geopy.distance.distance((lat,lng), (lat_cap,lng_cap)).km
    if dist > 100:
        return render_template('error_page.html', message='Your apartment is outside the DC metropolitan area.')
    
    #get "state" from address
    subregion_abbr = re.findall(r'"short_name"\s+:\s+"(.*)",\s+"types"\s+:\s+\[\s+"administrative_area_level_1"', geo_data)
    if subregion_abbr[0] == 'MD':
        subregion = 'maryland'
    elif subregion_abbr[0] == 'VA':
        subregion = 'northern virginia'
    else:
        subregion = 'district of columbia'
    
    #Predict prices------------------------------------------------
    X = pd.DataFrame({'br':float(bdrms), 'ba':float(baths), 'sqft':float(sqfootage), 'subregion':subregion}, index = range(1))
    
    f = open('./data/model.p', 'r')
    model = pickle.load(f)          
    f.close()

    price = model.predict(X)
    price_str = '%.2f' % price[0]
    
    #Get prices for histogram----------------------------------------
    f = open('./data/df_data.p', 'r')
    df = pickle.load(f)          
    f.close()
    
    df['price'] = df['price'].str[1:].astype(int)
    df = df[df['price'] <= 10000]
    
    dataDC = df[df['subregion'] == 'district of columbia']['price'].tolist()
    dataMD = df[df['subregion'] == 'maryland']['price'].tolist()
    dataVA = df[df['subregion'] == 'northern virginia']['price'].tolist()

    return render_template('results.html', data=price_str, dataDC=dataDC, dataMD=dataMD, dataVA=dataVA)
  
@app.route('/about_me')
def about_me():
  return render_template('about_me.html')

if __name__ == '__main__':
  port = int(os.environ.get('PORT',5000))
  app.run(host='0.0.0.0', port=port)
