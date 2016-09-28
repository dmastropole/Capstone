
# coding: utf-8

# # Exploratory Data Analysis: Dana's Capstone Project

# In[1]:

#for plotting
import numpy as np
import scipy.special
import pandas as pd

#for scraping 
from bs4 import BeautifulSoup
import requests
import re


# In[2]:

#for now, scrape craigslist data from zip code 02139
url = 'http://boston.craigslist.org/search/aap?search_distance=0&postal=02139&bedrooms=1'
print url

r = requests.get(url)


# In[3]:

r.status_code


# In[4]:

soup = BeautifulSoup(r.text)


# In[5]:

print soup.prettify()[1:100]


# In[6]:

'''Alternate way of doing it
prices = soup.select('span.price')
print prices
'''

prices = soup.find_all('span', attrs={'class':'price'})
print prices


# In[7]:

#parce out the prices 
regex = re.compile(r'<span class="price">\$(\d*)</span>')
price_list = []
for line in prices:
    m = regex.match(str(line))
    if m:
        price_list.append(int(m.groups()[0]))
print price_list
print len(price_list)


# In[8]:

#find number of bedrooms
room_attributes = soup.find_all('span', attrs={'class':'housing'})
print room_attributes
print len(room_attributes)


# In[9]:

#parce sq footage and number of bedrooms
regex2 = re.compile(r'<span class="housing">\n(?:\s*(\d*).*-\n){0,1}(?:\s*(\d*).*-\n){0,1}\s*</span>')
br_list = []
sqft_list = []
for line in room_attributes:
    m = regex2.match(str(line))
    if m:
        if m.groups()[0]!=None:
            br_list.append(int(m.groups()[0]))
        else:
            br_list.append(m.groups()[0])
        if m.groups()[1]!=None:
            sqft_list.append(int(m.groups()[1]))
        else:
            sqft_list.append(m.groups()[1])
    print line
    print m.groups()
print br_list
print sqft_list


# In[10]:

#create pandas dataframe
df = pd.DataFrame({'br' : br_list,
               'sqft' : sqft_list},
                 index=price_list)
df


# In[11]:

#import plotting libraries
import bokeh.plotting as bp
import matplotlib.pyplot as plt
from bokeh.io import output_notebook


# In[12]:

#import linear model
from sklearn import linear_model


# In[45]:

#create linear model
#x = df.index
#y = df['br']
x = np.array(price_list).reshape(1,-1)
y = np.array(br_list).reshape(1,-1)

regr = linear_model.LinearRegression()
regr.fit(x,y)

yfit = regr.predict(x)
print yfit


# In[27]:

output_notebook()


# In[52]:

print x
print y
print yfit

#convert fit to something bokeh can plot

    
p = bp.figure(title="Price-Bedroom Comparison", x_axis_label='Price', y_axis_label='Bedrooms')
r = p.scatter(price_list, br_list, color='#2222aa')
#s = p.scatter(price_list, yfit, color = 'red')

bp.show(p)


# In[ ]:



