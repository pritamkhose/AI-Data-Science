# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 12:14:48 2020

@author: Pritam
"""
import requests
from bs4 import BeautifulSoup
import os
import math
import numpy as np
import pandas as pd
import json

BaseURL = 'https://www.flipkart.com'
headers = {
    'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405'}
URL = 'https://www.flipkart.com/search?q=apple+mobiles&sid=tyy%2C4io&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_2_3_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_2_3_na_na_na&as-pos=2&as-type=RECENT&suggestionId=apple+mobiles%7CMobiles&requestId=d88030a1-2b0d-4256-89ef-4ea2da2728e7&as-searchtext=app'
page = requests.get(URL, headers)

soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find_all('div', class_='bhgxx2 col-12-12')

# jsonD = json.dumps(result.text)
# aList.append([index, jsonD, ''])

aList = []
for index, result in enumerate(results):
    print('index --> ' + str(index))

    ListImages = {}
    images = results[index].find_all('img')
    for i, image in enumerate(images):
        print('img --> ' + str(i))
        try:
            ListImages['alt'] = image['alt']
        except:
            ListImages['alt'] = None
        try:
            ListImages['src'] = image['src']
        except:
            ListImages['src'] = None
        print('img --> ' + str(ListImages))
        # ListImages.append([i, ListImages])
    if(index < 28):
        aList.append([index, results[index].find(
            'a', href=True)['href'], ListImages])
df = pd.DataFrame(aList, columns=['index', 'link', 'image'])
