# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 15:36:12 2020

@author: Pritam
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


compname = 'IT'
# url = 'https://www.moneycontrol.com/mc/widget/basicchart/get_chart_value?classic=true&dur=max&sc_did=' + compname
# datajson = requests.get(url).json()
# stock = datajson['g1']
# PVList = [];
# for row in range(len(stock)):
#     PVList.append([pd.to_datetime(stock[row]['date']), float(stock[row]['value']), float(stock[row]['open']) , float(stock[row]['close']), float(stock[row]['low']), float(stock[row]['high']), float(stock[row]['volume'])])
# df = pd.DataFrame(PVList ,columns =['date', 'value', 'open', 'close', 'low', 'high', 'volume']) 


# df.to_json(compname + 'day.json')

df = pd.read_json(compname + 'day.json')

df['P'] = (df['high'] + df['low'] + df['close'])/3
df.set_index('date', inplace = True) 

def calcHLOCV(df, sample):
    dfH = df.resample(sample).max()
    dfL = df.resample(sample).min()
    dfO = df.resample(sample).first()
    dfC = df.resample(sample).last()
    dfV = df.resample(sample).sum()
    
    PVList=[]
    for row in range(len(dfH)):
        if(not math.isnan(dfH['value'][row])) : # dfH['value'][row] !=  float('nan')
            PV = [dfH.index[row].strftime ("%Y-%m-%d %H:%M:%S"), dfH['value'][row], dfL['value'][row], dfO['value'][row], dfC['value'][row] , dfV['volume'][row]]
            PVList.append(PV)    
    return pd.DataFrame(PVList, columns =['date', 'high', 'low', 'open', 'close', 'volume']) #, 'vol_sum'

dfMall = calcHLOCV(df, 'M');

dfMall['P'] = dfMall['low'] #(dfMall['high'] + dfMall['low'] + dfMall['close'])/3
dfMall['qty'] = 10
dfMall['StockMPrice'] = dfMall['P'] * 10

dfMalllen = len(dfMall) - 1
dfM = dfMall[(dfMalllen-(12*20)):dfMalllen]
dfM.reset_index(inplace = True, drop = True) 

totalQTY = sum(dfM['qty'])
totalInvest = sum(dfM['StockMPrice'])
dfMlen = len(dfM)-1
lastPrice = dfM['high'][dfMlen]
todayValue = totalQTY * lastPrice
retrunTimes = todayValue/totalInvest
avgPrice= sum(dfM['P']) / len(dfM['P'])
retrunPerc = (todayValue * 100)/totalInvest
print(totalQTY, lastPrice, totalInvest, todayValue)
print(avgPrice, retrunTimes, retrunPerc)

# vper =  1000000 #df['Volume'].mean()*0.1
# #Visualize the data
# plt.figure(figsize=(16,8))
# plt.title('Stock ')
# plt.xlabel('Date', fontsize=10)
# plt.ylabel('Price', fontsize=10)
# plt.plot(df['value'], label = "Price", linewidth=1,)
# # plt.plot((df['volume']/vper), label = "Volume", linewidth=1,)
# plt.legend()
# plt.grid()
# plt.savefig("1.png")
# plt.show()    