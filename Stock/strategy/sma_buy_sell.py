# -*- coding: utf-8 -*-
"""
Created on Sun May 31 12:11:10 2020

@author: Pritam

https://www.youtube.com/watch?v=SEQbb8w7VTw&feature=youtu.be

https://matplotlib.org/3.2.1/api/markers_api.html
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
#url = 'https://www.moneycontrol.com/mc/widget/basicchart/get_chart_value?classic=true&dur=max&sc_did=' + compname
url = 'https://www.moneycontrol.com/mc/widget/basicchart/get_chart_value?classic=true&dur=5d&sc_did=' + compname
datajson = requests.get(url).json()
stock = datajson['g1']
PVList = [];
for row in range(len(stock)):
#    PVList.append([pd.to_datetime(stock[row]['date']), float(stock[row]['value']), float(stock[row]['volume'])])
    PVList.append([stock[row]['date'], float(stock[row]['value']), float(stock[row]['volume'])])
df = pd.DataFrame(PVList ,columns =['date', 'value', 'volume']) 

df['SMA30'] = df['value'].rolling(window=30).mean()
df['SMA50'] = df['value'].rolling(window=50).mean()

npnan = np.nan
def buy_sell(data):
    sigPriceBuy = []
    sigPriceSell = []
    flag = -1
    
    for i in range(len(data)):
        if data['SMA30'][i] > data['SMA50'][i] :
            if flag != 1:
                sigPriceBuy.append(data['value'][i])
                sigPriceSell.append(npnan)
                flag = 1
            else:
                sigPriceBuy.append(npnan)
                sigPriceSell.append(npnan)
        elif data['SMA30'][i] < data['SMA50'][i] :
             if flag != 0:
                sigPriceBuy.append(npnan)
                sigPriceSell.append(data['value'][i])
                flag = 0
             else:
                sigPriceBuy.append(npnan)
                sigPriceSell.append(npnan)
        else:
                sigPriceBuy.append(npnan)
                sigPriceSell.append(npnan)
    return(sigPriceBuy, sigPriceSell)
    
buysell = buy_sell(df)
df['sigPriceBuy'] = buysell[0]
df['sigPriceSell'] = buysell[1]

start = 1700;
end = len(df);
#Visualize the data
plt.figure(figsize=(16,8))
plt.title(compname + ' Stock')
plt.xlabel('Date', fontsize=10)
plt.ylabel('Close Price', fontsize=10)
plt.plot(df['value'][start:end], label = "Close Price", linewidth=1, color='blue')
plt.plot(df['SMA30'][start:end], label = "SMA30", linewidth=1, color='yellow')
plt.plot(df['SMA50'][start:end], label = "SMA50", linewidth=1, color='green')
#plt.plot((dffinal['gap'][0:1000] * vper), label = "gap", linewidth=1,)'
plt.scatter(df.index[start:end], df['sigPriceBuy'][start:end], label = "buy", marker= '^', color='green')
plt.scatter(df.index[start:end], df['sigPriceSell'][start:end], label = "sell", marker= 'v', color='red')

plt.legend()
plt.savefig("1.png")
plt.show()    