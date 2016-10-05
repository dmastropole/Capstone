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

#-------------------- FUNCTIONS

def scrape_data(latlon):
    #takes tuple (lat, lon)
    
    #load in dataframe
    f = open('./src/state_regions_df.p', 'r')
    df = pickle.load(f)          
    f.close()
    
    #get url
    coordinate_list = df['lat_lon'].tolist()
    pts = [ geopy.Point(p[0],p[1]) for p in coordinate_list ]
    onept = geopy.Point(latlon[0],latlon[1])
    alldist = [ (p,geopy.distance.distance(p, onept).km) for p in pts ]
    nearest_point = min(alldist, key=lambda x: (x[1]))[0]
    s = df['url']
    
    region_url = s[pts.index(nearest_point)]
    
    #figure out search extension
    url = 'http://webcache.googleusercontent.com/search?q=cache:http:' + region_url
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    info = soup.select('div.housing')
    ext = re.findall(r'\s+data-cat="apa"\s+href="(.*)"><span class="txt">apts / housing',str(info))
    ext = ext[0]
    if ext == '/i/apartments':
        url_intermediate = url[:-1] + ext
        r = requests.get(url_intermediate)
        #print r.status_code
        soup = BeautifulSoup(r.text, 'lxml')
        info = soup.select('ul.ul')
        extension = re.findall(r'href="(.*)">all\s+apartments',str(info))
        ext = extension
    
    #url for parent region
    url_listings = url[:-1] + ext
    
    #search subareas
    r = requests.get(url_listings)
    soup_subareas = BeautifulSoup(r.text, 'lxml')
    info = soup_subareas.select('select#subArea')
    
    extensions = re.findall(r'<option\s+value="(.*?)">(.*?)</option>',str(info))
    
    #initialize dataframe
    df_full = pd.DataFrame(columns=('dtime', 'br', 'ba', 'sqft', 'subregion', 'pnr', 'price'))
    
    #cycle through the subareas
    for abbr, region in extensions:
        sub_url = url_listings[:-3] + abbr + url_listings[-4:]
    
        r = requests.get(sub_url, 'lxml')
        soup_sub = BeautifulSoup(r.text, 'lxml')
    
        #get list of pages to cycle through
        totcount_info = soup_sub.select('span.totalcount')
        totcount = re.findall(r'"totalcount">(.*?)</span>',str(totcount_info[0]))[0]
        if int(totcount) < 500:
            pglist = range(100,int(totcount),100)
        else:
            pglist = range(100,500,100)
    
        for pg in pglist:
            pg_url = sub_url + '?s=' + str(pg)
            r_pg = requests.get(pg_url, 'lxml')
            soup_pg = BeautifulSoup(r_pg.text, 'lxml')
        
            info_pg = soup_pg.select('p.row')
            if info_pg:
                df = pd.DataFrame(np.nan, index=range(len(info_pg)), columns=('dtime', 'br', 'ba', 'sqft', 'subregion', 'pnr', 'price'))
                for i in range(len(info_pg)):
                    dtime = re.findall(r'<time\s+datetime="(.*?)"',str(info_pg[i]))
                    if dtime:
                        df.ix[i,'dtime'] = dtime[0]
                    price = re.findall(r'="price">(.*?)</span>',str(info_pg[i]))
                    if price:
                        df.ix[i,'price'] = price[0]
                    br = re.findall(r'(\d+)br',str(info_pg[i]))
                    if br:
                        df.ix[i,'br'] = br[0]
                    sqft = re.findall(r'(\d+)ft',str(info_pg[i]))
                    if sqft:
                        df.ix[i,'sqft'] = sqft[0]
                    pnr = re.findall(r'"pnr">\n<small>\s+(.*?)</small>',str(info_pg[i]))
                    if pnr:
                        df.ix[i,'pnr'] = pnr[0]
                    ba = re.findall(r'[0-9\.]\s+[Bb][ATHath][ROMSroms]|[0-9\.]\s+[Bb][Aa]',str(info_pg[i]))
                    if ba:
                        ba = re.findall(r'\d+',ba[0])
                        df.ix[i,'ba'] = ba[0]
                    df.ix[i,'subregion'] = region

                    #concatinate dataframes
                    df_full = pd.concat([df_full,df])
            
    #get rid of entries without a price        
    df_short = df_full.dropna(subset=['price'])
        
    #save dataframe
    f = open('./data/df_data.p', 'w')
    pickle.dump(df_short, f)          
    f.close()
    
    df_short.to_csv('./data/data.csv')
    
    return df_short
            
    
    
