#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  2 12:52:38 2022

@author: pritamkhose


https://www.moneycontrol.com/stocks/marketstats/indexcomp.php?optex=BSE&opttopic=indexcomp&index=33

https://www.moneycontrol.com/stocks/marketstats/indexcomp.php

"""

import os
import json
import pandas as pd

import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405'}

def getData():
    url = 'https://www.moneycontrol.com/stocks/marketstats/indexcomp.php'
    page = requests.get(url, headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    index_results_row = soup.find_all('div', class_='lftmenu')[0].find_all('a')
    indexList = []
    for index, link in enumerate(index_results_row):
        url = str(link.get("href"))
        if 'stocks' in url : 
            indexList.append(url)

    aList = []
    for url in indexList:
        print(url)
        page = requests.get('https://www.moneycontrol.com' +url, headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        results_row = soup.find_all('table', class_='tbldata14 bdrtpg')[0].find_all('tr')
        for index, result in enumerate(results_row):
            trs = result.find_all('td')
            if len(trs) > 0:
                cname = trs[0].find_all('a', href=True)[0].text
                clink = trs[0].find_all('a', href=True)[0]['href']
                idarr = clink.split("/")
                cid=idarr[len(idarr)-1]
                aList.append([index, cid, cname, clink, trs[1].text, trs[2].text.replace(',',''), trs[3].text, trs[4].text, trs[5].text.replace(',','')])
    
    
    df = pd.DataFrame(aList, columns=['i', 'id', 'name', 'link', 'industry', 'price', 'chg', 'pChg', 'mktCr'])
    df['price'] = df['price'].astype(float)
    #df['chg'] = df['chg'].astype(float)
    #df['pChg'] = df['pChg'].astype(float)
    df['mktCr'] = df['mktCr'].astype(float)
    
    # Writing json file
    with open("IndexCompNames.json", "w") as outfile: 
        outfile.write(df.to_json(orient ='records')) 

# remove duplicate
df = pd.DataFrame(json.load(open('IndexCompNames.json', 'r')))
df = df.drop_duplicates(['id','name'], keep='last')
df = df.sort_values(by = ['mktCr'], ascending = False)
df = df.drop('i', axis=1)
df = df.reset_index(drop=True)
# Writing json file
with open("IndexCompNamesFinal.json", "w") as outfile: 
    outfile.write(df.to_json(orient ='records')) 
df.to_csv('IndexCompNamesFinal.csv')