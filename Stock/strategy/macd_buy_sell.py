# -*- coding: utf-8 -*-
"""
Created on Sun May 31 15:13:05 2020

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

df['EMA_9'] = df['value'].ewm(span=9,adjust=False).mean()
df['EMA_12'] = df['value'].ewm(span=12,adjust=False).mean()
df['EMA_26'] = df['value'].ewm(span=26,adjust=False).mean()
    
df['macd'] = df['EMA_12'] - df['EMA_26']
df['signal'] = df['macd']*(2/(df['EMA_9']+1))+df['macd'].shift(-1)*(1-(2/(df['EMA_9']+1)))
df['histogram'] =  df['macd'] - df['signal']
    
npnan = np.nan
def buy_sell(data):
    sigPriceBuy = []
    sigPriceSell = []
    flag = -1
    
    for i in range(len(data)):
        if data['macd'][i] < data['signal'][i] : # df['histogram'] > 0 :
            if flag != 1:
                sigPriceBuy.append(data['value'][i])
                sigPriceSell.append(npnan)
                flag = 1
            else:
                sigPriceBuy.append(npnan)
                sigPriceSell.append(npnan)
        elif data['macd'][i] > data['signal'][i] : # df['histogram'] < 0 :
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

start = 1500;
end = len(df);
#Visualize the data

fig, axs = plt.subplots(3, figsize=(20, 10))
fig.suptitle(compname + ' Stock')
#plt.title(compname + ' Stock')
#plt.xlabel('Date', fontsize=10)
#plt.ylabel('Close Price', fontsize=10)
axs[0].plot(df['value'][start:end], label = "Close Price", linewidth=1, color='blue')
axs[0].scatter(df.index[start:end], df['sigPriceBuy'][start:end], label = "buy", marker= '^', color='green')
axs[0].scatter(df.index[start:end], df['sigPriceSell'][start:end], label = "sell", marker= 'v', color='red')

axs[1].plot(df['macd'][start:end], label = "macd", linewidth=1, color='green')
axs[1].plot(df['signal'][start:end], label = "signal", linewidth=1, color='red')

axs[2].bar(df.index[start:end], df['histogram'][start:end], label = "histogram")
fig.legend()
fig.savefig("1.png")
fig.show()    