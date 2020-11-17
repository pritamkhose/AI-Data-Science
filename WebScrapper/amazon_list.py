# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 11:15:56 2020

@author: Pritam
"""
import requests
from bs4 import BeautifulSoup
import os
import math
import numpy as np
import pandas as pd
import json
from pathlib import Path
path = Path(os.path.dirname(os.path.realpath(__file__)))

BaseURL = 'https://www.amazon.in/'
headers = {
    'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405'}
URL = 'https://www.amazon.in/s/ref=lp_16613114031_il_ti_electronics?rh=n%3A976419031%2Cn%3A%211499770031%2Cn%3A%211499772031%2Cn%3A%2120348478031%2Cn%3A16613114031&ie=UTF8&qid=1605073486&lo=electronics'
page = requests.get(URL, headers)

soup = BeautifulSoup(page.content, 'html.parser')

listresult = soup.findAll('div', id='mainResults')
listresult = listresult[0].findAll('div', attrs={'class': 's-item-container'})
alist = listresult

print(alist)
products = []
for index, div in enumerate(alist):
    productitem = {}
    productitem['index'] = index
    productitem['url'] = div.find('a', href=True)['href']
    productitem['name'] = div.find('h2').text
    productitem['imgurl'] = div.find('img')['src']
    productitem['price'] = str(div.find_all(
        'span', class_='a-size-base a-color-price s-price a-text-bold')[0].text).replace("\xa0\xa0", '')
    products.append(productitem)

# Writing to json file
with open('amazonlist' + '.json', 'w') as outfile:
    outfile.write(json.dumps(products))
