# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 11:27:22 2020

@author: Pritam

https://api.bseindia.com/BseIndiaAPI/api/GetMktData/w?ordcol=TT&strType=index&strfilter=S%26P+BSE+500

"""


#Import the libraries
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#plt.style.use('fivethirtyeight')
import json
import requests

#if not os.path.exists('data'):
#    os.makedirs('data')
## Writing to json file
#with open('data/bseAll.json', 'w') as outfile: 
#    outfile.write(json.dumps(datajson))
   

url =  'https://api.bseindia.com/BseIndiaAPI/api/GetMktData/w?ordcol=TT&strType=index&strfilter=S%26P+BSE+500'
datajson = (requests.get(url).json()['Table'])

PVList = []
for row in range(len(datajson)):
    name =  datajson[row]['URL'].replace("https://www.bseindia.com/stock-share-price/", "").split("/")[0].replace("-", " ").replace(" ltd", " ")
    PVList.append([datajson[row]['scripname'], datajson[row]['scrip_cd'], name, datajson[row]['URL']])
bsedf = pd.DataFrame(PVList, columns =['scripname','scrip_cd', 'name', 'url']) 

#headers = {'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405'}
#url =  'https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20500'
#datajson = requests.get(url, headers=headers).json()['data']
#PVList = []
#for row in range(len(datajson)):
#    PVList.append([datajson[row]['symbol'], datajson[row]['identifier'], str(datajson[row]['meta'])])
#nsedf = pd.DataFrame(PVList, columns =['symbol','companyName', 'identifier']) 


url =  'https://pritam-node.herokuapp.com/RestAPIMongoDBAll?Database=moneycontrol&Collection=listCompanies'
datajson = (requests.get(url).json())
PVList = []
for row in range(len(datajson)):
    PVList.append([datajson[row]['id'], datajson[row]['name'],  datajson[row]['link']])
moneydf = pd.DataFrame(PVList, columns =['id','name', 'URL']) 
PVList = []

s1 = pd.merge(moneydf, bsedf, how='inner', on=['name'])

#df_row = pd.concat([moneydf, bsedf], axis=1)
#
#print(len(moneydf), len(bsedf), len(moneydf)+ len(bsedf) )