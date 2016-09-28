
# coding: utf-8

# In[1]:

#for plotting
import numpy as np
import scipy.special
import pandas as pd

#for scraping 
from bs4 import BeautifulSoup
import requests
import re

#for saving data
import pickle


# In[2]:

#scrape data
base_url = 'http://boston.craigslist.org/search/aap?search_distance=0&postal=02139&bedrooms=1'
r_base = requests.get(base_url)
r_base.status_code


# In[3]:

#get html strings
soup_base = BeautifulSoup(r_base.text, 'lxml')
housing_html = soup_base.select('p.row span.housing')
price_html = soup_base.select('p.row span.price')

#parse out bedrooms, bathrooms, and price
regex_housing = re.compile(r'<span class="housing">\n(?:\s*(\d*).*-\n){0,1}(?:\s*(\d*).*-\n){0,1}\s*</span>')
regex_price = re.compile(r'<span class="price">\$(\d*)</span>')

#get data into nice list
br_list = []
sqft_list = []
price_list = []
for line in price_html:
    m_price = regex_price.match(str(line))
    if m_price:
        price_list.append(int(m_price.groups()[0]))
    else:
        price_list.append('None')
for line in housing_html:
    m_housing = regex_housing.match(str(line))
    if m_housing:
        if m_housing.groups()[0]!=None:
            br_list.append(int(m_housing.groups()[0]))
        else:
            br_list.append('None')
        if m_housing.groups()[1]!=None:
            sqft_list.append(int(m_housing.groups()[1]))
        else:
            sqft_list.append('None')
print len(price_list)
print len(br_list)
print len(sqft_list)


# In[4]:

#create pandas dataframe
df = pd.DataFrame({'br' : br_list,
               'sqft' : sqft_list},
                 index=price_list)
df


# In[5]:

#pickle party paths
f = open('data.p', 'w')
pickle.dump(df, f)          
f.close() 

