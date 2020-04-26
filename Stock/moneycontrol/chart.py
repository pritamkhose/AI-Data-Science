# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 11:27:22 2020

@author: Pritam
https://www.geeksforgeeks.org/pandas-parsing-json-dataset/

https://www.moneycontrol.com/mc/widget/basicchart/get_chart_value?classic=true&sc_did=SBI&dur=1d

https://www.moneycontrol.com/tech_charts/nse/his/sbi.csv?classic=true
https://www.moneycontrol.com/tech_charts/bse/his/sbi.csv?classic=true
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
compname = 'SBI'
url = 'https://www.moneycontrol.com/mc/widget/basicchart/get_chart_value?classic=true&dur=max&sc_did=' + compname
datajson = requests.get(url).json()

if not os.path.exists('data'):
    os.makedirs('data')
# Writing to json file
with open('data/'+compname + '.json', 'w') as outfile: 
    outfile.write(json.dumps(datajson))
# Read to json file
with open('data/'+compname + '.json') as json_file:
    datajson = json.load(json_file)

#newsdata = datajson['newsdata']
#data = datajson['data']
stock = datajson['g1']
PVList = [];
for row in range(len(stock)):
    PVList.append([pd.to_datetime(stock[row]['date']), float(stock[row]['value']), float(stock[row]['open']) , float(stock[row]['close']), float(stock[row]['low']), float(stock[row]['high']), float(stock[row]['volume'])])
df = pd.DataFrame(PVList ,columns =['date', 'value', 'open', 'close', 'low', 'high', 'volume']) 
# for 5d
#    PVList.append([stock[row]['date'], float(stock[row]['value']), float(stock[row]['volume'])])
#df = pd.DataFrame(PVList ,columns =['date', 'value', 'volume']) 

df.to_json('data/'+compname + '1.json')

df.index = df['date']

vper =  1000000 #df['Volume'].mean()*0.1
#Visualize the data
plt.figure(figsize=(16,8))
plt.title('Stock ')
plt.xlabel('Date', fontsize=10)
plt.ylabel('Price', fontsize=10)
plt.plot(df['value'], label = "Price", linewidth=1,)
plt.plot((df['volume']/vper), label = "Volume", linewidth=1,)
plt.legend()
plt.grid()
plt.savefig("1.png")
plt.show()    