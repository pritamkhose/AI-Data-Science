# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 13:25:04 2020

@author: Pritam

https://www.twilio.com/blog/web-scraping-and-parsing-html-in-python-with-beautiful-soup
https://stackoverflow.com/questions/38489386/python-requests-403-forbidden
https://stackoverflow.com/questions/11709079/parsing-html-using-python
https://stackoverflow.com/questions/6287529/how-to-find-children-of-nodes-using-beautifulsoup
"""

import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

aurl = 'https://www.bseindia.com/sensex/Index_Contribution.aspx?index_code=16'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
html_text = requests.get(aurl, headers=headers).text
soup = BeautifulSoup(html_text, 'html.parser')

sensexvalue = soup.body.find('span', attrs={'class' : 'viewsensexvalue'}).text
print(sensexvalue)

sensexgreentext = soup.body.find('span', attrs={'class' : 'sensexgreentext'}).text
print(sensexgreentext)

tablediv = soup.body.find('div', attrs={'class' : 'col-lg-12 largetable'})
print(tablediv)

table = tablediv.find('table')
table_rows = table.find_all('tr')
print(table_rows)

l = []
skipcount = 0
for tr in table_rows:
    td = tr.find_all('td')
    row = [tr.text for tr in td]
    skipcount = skipcount + 1
    if skipcount > 2:
        l.append(row)
df = pd.DataFrame(l, columns =['Code', 'Company', 'LTP', 'Change', 'PtsContribution']) 

df['Code'] = pd.to_numeric(df['Code'])
df['LTP'] = pd.to_numeric(df['LTP'])
df['Change'] = pd.to_numeric(df['Change'])
df['PtsContribution'] = pd.to_numeric(df['PtsContribution'])
df['PtsContChange'] = df['Change'] / df['PtsContribution']