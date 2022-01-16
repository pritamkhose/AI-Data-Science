# -*- coding: utf-8 -*-
"""
Created on Sat Jan 15 16:49:27 2022

@author: Pritam

https://stackoverflow.com/questions/63981362/python-requests-get-returns-response-code-401-for-nse-india-website

https://archives.nseindia.com/content/indices/ind_nifty500list.csv

https://www.nseindia.com/market-data/live-equity-market?symbol=NIFTY%2050
"""

#Import the libraries
import math
import numpy as np
import pandas as pd
import os
import json
import requests

fname =  'NIFTY500.json'

def getData():
    baseurl = "https://www.nseindia.com/"
    # url = f"https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
    url = f"https://www.nseindia.com/api/equity-stockIndices?index=NIFTY500%20MULTICAP%2050%3A25%3A25"
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                             'like Gecko) '
                             'Chrome/80.0.3987.149 Safari/537.36',
               'accept-language': 'en,gu;q=0.9,hi;q=0.8', 'accept-encoding': 'gzip, deflate, br'}
    session = requests.Session()
    request = session.get(baseurl, headers=headers, timeout=5)
    cookies = dict(request.cookies)
    response = session.get(url, headers=headers, timeout=5, cookies=cookies)
    datajson = response.json()
    print(datajson)
    
    
    if not os.path.exists('data'):
        os.makedirs('data')
    # Writing to json file
    with open('data/'+fname, 'w') as outfile: 
        outfile.write(json.dumps(datajson))


# returns JSON object as  a dictionary
data = json.load(open('data/'+fname))['data']
data = pd.DataFrame(data)