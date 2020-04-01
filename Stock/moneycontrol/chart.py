# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 11:27:22 2020

@author: Pritam
https://www.moneycontrol.com/mc/widget/basicchart/get_chart_value?classic=true&sc_did=SBI&dur=1d
"""


#Import the libraries
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#plt.style.use('fivethirtyeight')
import json
import requests

url = 'https://www.moneycontrol.com/mc/widget/basicchart/get_chart_value?classic=true&sc_did=SBI&dur=max'
datajson = requests.get(url).json()
#newsdata = datajson['newsdata']
#data = datajson['data']
stock = datajson['g1']
PVList = [];
for row in range(len(stock)):
    PVList.append([row, pd.to_datetime(stock[row]['date']), float(stock[row]['value']), float(stock[row]['open']) , float(stock[row]['close']), float(stock[row]['low']), float(stock[row]['volume'])])
df = pd.DataFrame(PVList, columns =['index','date', 'value', 'open', 'close', 'low', 'volume']) 

vper =  1000000 #df['Volume'].mean()*0.1
#Visualize the data
plt.figure(figsize=(16,8))
plt.title('Stock ')
plt.xlabel('Date', fontsize=10)
plt.ylabel('Price', fontsize=10)
plt.plot(df['index'], df['value'], label = "Price", linewidth=1,)
plt.plot((df['volume']/vper), label = "Volume", linewidth=1,)
plt.legend()
plt.grid()
plt.savefig("1.png")
plt.show()    