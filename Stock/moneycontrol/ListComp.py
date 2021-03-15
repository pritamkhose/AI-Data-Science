# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 19:36:20 2021

@author: Pritam
"""


#Import the libraries
import os
import numpy as np
import pandas as pd
import json
import requests
from bs4 import BeautifulSoup

# # url =  'https://api.bseindia.com/BseIndiaAPI/api/GetMktData/w?ordcol=TT&strType=index&strfilter=S%26P+BSE+200'
# # headers = { 'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",}
# # data = requests.get(url, headers=headers).json()
# # f = open('bse200.json', "w")
# # f.write(json.dumps(data))
# # f.close()

# bseObj = json.load(open('bse200.json'))
# bseObj = bseObj['Table']
# bseDF = pd.DataFrame(bseObj)
# bseDF = bseDF[['scrip_cd', 'scripname', 'URL']] # , 'scrip_grp' 'index_code'
# bseDF['bsecmpname'] = bseDF['scripname'].str.lower()
# bseDF = bseDF.sort_values('bsecmpname')
# bseDF.reset_index(inplace = True)
# bseDF.drop('bsecmpname', axis=1, inplace=True)


# hit url brower and save file
# # https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20200
# nseObj = json.load(open('NIFTY200.json'))
# nseObj = nseObj['data']
# del nseObj[0]
# nseDF = pd.DataFrame(nseObj)
# nseDF = nseDF[['symbol', 'identifier']]
# nseDF['nsecmpname'] = nseDF['identifier'].str.lower()
# nseDF = nseDF.sort_values('nsecmpname')
# nseDF.reset_index(inplace = True)
# nseDF.drop('nsecmpname', axis=1, inplace=True)

# # mcurl =  'https://api.bseindia.com/BseIndiaAPI/api/GetMktData/w?ordcol=TT&strType=index&strfilter=S%26P+BSE+200'
# # page = requests.get(mcurl)
# # soup = BeautifulSoup(page.content, 'html.parser')
# # with open("mc.html",  "w", encoding='utf-8') as file:
# #     file.write(str(soup))

# # Goto url > inspect element > copy table html> paste in file
# HtmlFile = open('mc.html', 'r', encoding='utf-8')
# source_code = HtmlFile.read()
# soup = BeautifulSoup(source_code, 'html.parser')

# # http://www.moneycontrol.com/india/stockpricequote/autolcvshcvs/tatamotors/TM03
# alist = []
# for link in soup.findAll("a"):
#     name = link.text
#     mccmpname = name.replace(" ", '').lower()
#     url = link.get("href")
#     if('stockpricequote' in url):
#         alist.append([mccmpname, name, url])
# mcdf = pd.DataFrame(alist, columns =['mccmpname', 'mcName', 'mcURL'])
# mcdf = mcdf.sort_values('mccmpname')
# mcdf.reset_index(inplace = True)
# mcdf.drop('mccmpname', axis=1, inplace=True)


# res = pd.concat([mcdf, bseDF], axis=1)
# res.drop('index', axis=1, inplace=True)
# res.to_json('comp200.json', orient='records')

comp200R = json.load(open('comp200R.json'))
comp200RDF = pd.DataFrame(comp200R)
alist = []
for i, row in comp200RDF.iterrows():
    name = row['mcURL'].split("/")[7]
    alist.append([row['mcName'], name])
mcdfCode = pd.DataFrame(alist, columns =['mcNameTemp', 'mcCode'])
result = pd.concat([comp200RDF, mcdfCode], axis=1)
result.drop('mcNameTemp', axis=1, inplace=True)
result.to_json('comp200R2.json', orient='records')
