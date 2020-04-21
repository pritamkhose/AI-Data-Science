# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 11:27:22 2020

@author: Pritam
https://appfeeds.moneycontrol.com/jsonapi/market/graph&format=json&ind_id=9&range=max&type=area

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

#1d 5d max
compname = 'NIFty50'
#url = 'https://appfeeds.moneycontrol.com/jsonapi/market/graph&format=json&ind_id=9&range=max&type=area'
#datajson = requests.get(url).json()
#
#if not os.path.exists('data'):
#    os.makedirs('data')
## Writing to json file
#with open('data/'+compname + '.json', 'w') as outfile: 
#    outfile.write(json.dumps(datajson))
# Read to json file
with open('data/'+compname + '.json') as json_file:
    datajson = json.load(json_file)


stock = datajson['graph']['values']
PVList = [];
for row in range(len(stock)):
    time = pd.to_datetime(stock[row]['_time'])
    value = float(stock[row]['_value'])
    openV = float(stock[row]['_open'])
    close = float(stock[row]['_close'])
    low = float(stock[row]['_low'])
    high = float(stock[row]['_high'])
    volume = float(stock[row]['_volume'])
    PVList.append([time, value, openV, close, low, high, volume ])
df = pd.DataFrame(PVList ,columns =['time', 'value', 'open', 'close', 'low', 'high', 'volume']) 

# calculate
PVList=[]
for row in range(len(df)):
    if(row == 0):
        gap = 0
    else:
        gap = df['open'][row] - df['close'][row-1]
    PVList.append([gap])    
df1 = pd.DataFrame(PVList, columns =['gap']) 

dffinal = df1.join(df)
dffinal.index = df['time']
#df.to_json('data/'+compname + '1.json')

vper =  ((dffinal['gap'].max() - dffinal['gap'].min()) /2 ) * 0.01 * 10

#Visualize the data
plt.figure(figsize=(16,8))
plt.title('Stock ')
plt.xlabel('Date', fontsize=10)
plt.ylabel('Price', fontsize=10)
plt.plot(dffinal['value'][0:1000], label = "Price", linewidth=1,)
plt.plot((dffinal['gap'][0:1000] * vper), label = "gap", linewidth=1,)
plt.legend()
plt.grid()
plt.savefig("1.png")
plt.show()    