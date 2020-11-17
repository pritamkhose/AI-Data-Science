# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 18:16:27 2020

@author: Pritam

https://medium.com/edureka/web-scraping-with-python-d9e6506007bf
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
URL = 'https://www.flipkart.com/laptops/~buyback-guarantee-on-laptops-/pr?sid=6bo%2Cb5g&uniqBStoreParam1=val1&wid=11.productCard.PMU_V2'
page = requests.get(URL, headers)

soup = BeautifulSoup(page.content, 'html.parser')

# results = soup.find_all('div', class_='bhgxx2 col-12-12')
products = []
for a in soup.findAll('a', href=True, attrs={'class': '_31qSD5'}):
    name = a.find('div', attrs={'class': '_3wU53n'})
    price = a.find('div', attrs={'class': '_1vC4OE _2rQ-NK'})
    rating = a.find('div', attrs={'class': 'hGSR34 _2beYZw'})
    products.append([name.text, price.text, rating.text])
