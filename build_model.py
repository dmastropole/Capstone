#for saving data
import pickle

#pandas
import pandas as pd

#numpy
import numpy as np

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

#load data
f = open('./data/df_data.p', 'r')
df = pickle.load(f)          
f.close() 

#change data-type of prices and eliminate unreasonable values
df['price'] = df['price'].str[1:].astype(int)
df = df[df['price'] <= 10000]

#split dataframe into predictors and outcomes
y = df['price']
X = df.drop('price',1) 

#build model
fullModel = pipeline.Pipeline([("col_select", categoryTransformer(['sqft','br','ba'])),
                               ("imp",Imputer(missing_values='NaN', strategy='median', axis=0)),
                               ("lin",LinearRegression())
        
    ])
    
#cross validate
param_grid_pipeline = {'lin__fit_intercept':[True,False], 'lin__normalize':[True,False]}

grid = GridSearchCV(fullModel, param_grid_pipeline, cv = 5, n_jobs = -1, verbose=1, scoring = 'mean_squared_error')

grid.fit(X, y)

#save model
f = open('./data/model.p', 'w')
pickle.dump(fullModel, f)          
f.close() 

