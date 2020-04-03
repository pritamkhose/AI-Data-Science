# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 11:27:22 2020

@author: Pritam
https://charting.bseindia.com/index.html?SYMBOL=532174#

https://www.nseindia.com/api/historical/cm/equity?symbol=INFY&series=[%22EQ%22]&from=02-04-2019&to=02-04-2020

"""

#Import the libraries
import os
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#plt.style.use('fivethirtyeight')
import json
import requests

headers = {'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405'}
compname = 'INFYEQN'
url = 'https://www.nseindia.com/api/chart-databyindex?index=' + compname
datajson = requests.get(url, headers=headers).json()

if not os.path.exists('data'):
    os.makedirs('data')
# Writing to json file
with open('data/'+compname + '.json', 'w') as outfile: 
    outfile.write(json.dumps(datajson))
# Read to json file
with open('data/'+compname + '.json') as json_file:
    datajson = json.load(json_file)
    
datainval = datajson['grapthData']
PVList=[]
for row in range(len(datainval)):
    PVList.append([ row, pd.to_datetime(datainval[row][0]), datainval[row][1]])
df = pd.DataFrame(PVList, columns =['index','date', 'price']) 
df.index = df['date']

#Visualize the data
plt.figure(figsize=(16,8))
plt.title('Stock ')
plt.xlabel('Date', fontsize=10)
plt.ylabel('Price', fontsize=10)
plt.plot(df['price'], label = "Price", linewidth=1,)
plt.legend()
plt.grid()
plt.savefig("1.png")
plt.show()    