#for scraping 
from bs4 import BeautifulSoup
import requests
import re

#for saving data
import pickle

#pandas
import pandas as pd

#------------------ Scrape States and Regions
#build url and get information
sites_url = 'http://webcache.googleusercontent.com/search?q=cache:http://www.craigslist.org/about/sites'
r_sites = requests.get(sites_url)
soup_sites = BeautifulSoup(r_sites.text, 'lxml')

#create nested dictionary of states and regions
boxes = ['div.box.box_1','div.box.box_2','div.box.box_3','div.box.box_4']
state_dict = {}

for box in boxes:
    info = soup_sites.select(box)
    info = info[0]
    state_regions = re.findall(r'<h4>(.*?)</h4>\n<ul>((?:\n.*)+?\n</ul>)',str(info))
    
    for state, region in state_regions:
        url_city = re.findall(r'<li><a\s+href="(.*?)">(.*?)</a></li>',region)
        city_dict = {}
        city_list = []
        url_list = []
        for url, city in url_city:
            city_list.append(city)
            url_list.append(url)
        city_dict['city'] = city_list
        city_dict['url'] = url_list
        state_dict[state] = city_dict

#add information to dataframe
df =pd.DataFrame.from_dict(state_dict,orient='index')

s1 = df.apply(lambda x: pd.Series(x['city']),axis=1).stack().reset_index(level=1, drop=True)
s2 = df.apply(lambda x: pd.Series(x['url']),axis=1).stack().reset_index(level=1, drop=True)
s1.name = 'region'
s2.name = 'url'
df_new = pd.concat([s1, s2], axis=1)

df_new['lat_lon'] = df.apply(lambda _: '', axis=1)
df_new.set_index('region', append=True, inplace=True)

#----------------- Google API: get lat and lon
api_key = '&key=AIzaSyCyYqXfiJLjQwRSS9PvKpWvfvnxP0A6Sw0'
base_url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' 


for index, row in df_new.iterrows():
    region = index[1].split('/')
    address = "+".join(region[0].split()) + '+' + "+".join(index[0].split())
    full_url = base_url + address + api_key
    
    r_ll = requests.get(full_url)
    geo_data= r_ll.content
    latlon = re.findall(r'"location"\s+:\s+{\s+"lat"\s+:\s+(.*),\s+"lng"\s+:\s+(.*)\s+}', geo_data)
    
    print index
    print latlon
    if not latlon:
        address = "+".join(index[0].split())
        full_url = base_url + address + api_key
    
        r_ll = requests.get(full_url)
        geo_data= r_ll.content
        latlon = re.findall(r'"location"\s+:\s+{\s+"lat"\s+:\s+(.*),\s+"lng"\s+:\s+(.*)\s+}', geo_data)
        
        df_new.set_value(index,'lat_lon',latlon[0])
    else:
        df_new.set_value(index,'lat_lon',latlon[0])
        
#------------------ Save
f = open('./data/state_regions_df.p', 'w')
pickle.dump(df_new, f)          
f.close() 

df_new.to_csv('./data/states_regions.csv')
