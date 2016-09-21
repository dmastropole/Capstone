from flask import Flask, render_template, request, redirect
import requests
import simplejson as json
import re

import numpy as np
import scipy.special
import pandas as pd

app = Flask(__name__)

@app.route('/')
def main():
  return render_template('main.html')

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
    zipcode = request.form['zipcode']
    bdrms = request.form['bdrms']
    baths = request.form['baths']
    
    #ZIPCODE API
    api_key = 'htn05QPh3vokALrY8T2RgaOd2Um4hMtzfQzlGpCKV14vMvtUpwMFHBTJvgON2hni'
    url = 'https://www.zipcodeapi.com/rest/'
    url = url + api_key + '/info.json/' + zipcode +'/degrees'
    
    r = requests.get(url=url)
    dataset = json.loads(r.content)
    
    lat = dataset['lat']
    lng = dataset['lng']
    coordinates = '(' + str(lng) + ',' + str(lat) +')'
    
    #CRAIGSLIST API
    url = 'http://www.rentrent.org/RENT/Ads.aspx?'
    xmin = lng - 0.1
    xmax = lng + 0.1
    ymin = lat - 0.1
    ymax = lat + 0.1
    
    url = url + 'xmin=' + str(xmin) + '&ymin=' + str(ymin) + '&xmax=' + str(xmax) + '&ymax=' + str(ymax) + '&bd=' + str(bdrms) + '&ba=' + str(baths) + '&pets=-1&type=2&throwErrorIfOverLimit=false&callback=xxx'
    r = requests.get(url=url)
    data = r.content
    prices = re.findall(r'&#x0024;(\d+)', data)
    
    #convert prices to integers
    prices = [float(i) for i in prices]
    mean_price = np.mean(prices)
    price_str = '%.2f' % mean_price
    
    return render_template('results.html', coordinates=coordinates, data=price_str)

@app.route('/about_me')
def about_me():
  return render_template('about_me.html')

if __name__ == '__main__':
  app.run(debug=True)