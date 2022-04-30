# -*- coding: utf-8 -*-
"""
Created on Sun Apr  3 17:31:45 2022

@author: Pritam

https://www.rbi.org.in/Scripts/bs_viewcontent.aspx?Id=2009
"""

import requests
from bs4 import BeautifulSoup
import os
import numpy as np
import pandas as pd
import json
import wget
# from pathlib import Path
# path = Path(os.path.dirname(os.path.realpath(__file__)))

# headers = {
#     'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405'}
# URL = 'https://www.rbi.org.in/Scripts/bs_viewcontent.aspx?Id=2009'
# cookies = dict(cookies_are='working')
# page = requests.get(URL, headers, cookies=cookies)

with open("banklist.html", "r", encoding='utf-8') as f:
    text= f.read()

soup = BeautifulSoup(text, 'html.parser')
#listresult = soup.find('div', id='example-min').find('div').find('table').find('tbody')

# li = soup.find('table', {'class': 'tablebg'})
# for child in li.children:
#     print(child)
# print(len(li))


urlList = []
listresult = soup.findAll("a", href=True)
for index, alink in enumerate(listresult):
    urlList.append(alink.attrs.get("href"))

try: 
    os.mkdir('banklist') 
except OSError as error: 
    print(error)  

i = 0;
for url in urlList:
    try:
        i+=1
        print(str(i) + ' - ' + url)
        wget.download(url, out='banklist')
    except: 
        print('error > '+ str(i))  

