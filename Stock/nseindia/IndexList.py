# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 11:27:22 2020

@author: Pritam

https://www.nseindia.com/json/derivatives.json
https://www.nseindia.com/json/live-index.json
https://www.nseindia.com/api/home-corporate-announcements?index=homepage
https://www.nseindia.com/api/marketStatus

https://www.nseindia.com/api/chart-databyindex?index=NIFTY%2050&indices=true

https://www.nseindia.com/api/allIndices
https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050
https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20500
https://www.nseindia.com/json/equity-stockIndices.json
https://archives.nseindia.com/content/indices/ind_nifty500list.csv

"""


#Import the libraries
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
import os
import json
import requests

headers = {'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405'}
#headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
#headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 5 Build/LMY48B; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.65 Mobile Safari/537.36'}
url =  'https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050'
datajson = requests.get(url, headers=headers).json()
fname =  (datajson['name'] + '-'+ datajson['timestamp']).replace('.', '').replace(':', '-')+ '.json'


if not os.path.exists('data'):
    os.makedirs('data')
# Writing to json file
with open('data/'+fname, 'w') as outfile: 
    outfile.write(json.dumps(datajson))
