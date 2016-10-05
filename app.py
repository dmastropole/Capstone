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
from datetime import datetime
import pandas as pd
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
    
    #Get lat and lon from address
    address = '+'.join(address.split())
    api_key = '&key=AIzaSyCyYqXfiJLjQwRSS9PvKpWvfvnxP0A6Sw0'
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json?address='
    full_url = base_url + address + api_key
    r = requests.get(full_url)
    geo_data = r.content
    #geo_data = geo_data.decode("utf-8") 
    latlon = re.findall(r'"location"\s+:\s+{\s+"lat"\s+:\s+(.*),\s+"lng"\s+:\s+(.*)\s+}', geo_data)
    lat = float(latlon[0][0].strip("'"))
    lng = float(latlon[0][1].strip("'"))
    
    #Scrape craigslist using lat and lon
    #latlon = (float(lat),float(lng))
    #df = scrape_data(latlon)
    
    #Build model
    #build_model()
    
    #Predict prices
    X = pd.DataFrame({'br':float(bdrms), 'ba':float(baths), 'sqft':float(sqfootage)}, index = range(1))
    
    f = open('./data/model.p', 'r')
    model = pickle.load(f)          
    f.close()

    price = model.predict(X)
    price_str = '%.2f' % price[0]

    return render_template('results.html', data=price_str)

@app.route('/about_me')
def about_me():
  return render_template('about_me.html')

if __name__ == '__main__':
  port = int(os.environ.get('PORT',5000))
  app.run(host='0.0.0.0', port=port)
