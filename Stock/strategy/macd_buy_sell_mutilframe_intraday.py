# -*- coding: utf-8 -*-
"""
Created on Sun May 31 16:33:01 2020

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

# Get Data
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

# Function
def caculate_macd(df, pricetype):
    df['EMA_9'] = df[pricetype].ewm(span=9,adjust=False).mean()
    df['EMA_12'] = df[pricetype].ewm(span=12,adjust=False).mean()
    df['EMA_26'] = df[pricetype].ewm(span=26,adjust=False).mean()
        
    df['macd'] = df['EMA_12'] - df['EMA_26']
    df['signal'] = df['macd']*(2/(df['EMA_9']+1))+df['macd'].shift(-1)*(1-(2/(df['EMA_9']+1)))
    df['histogram'] =  df['macd'] - df['signal']
    return df
    
npnan = np.nan
def buy_sell(data, pricetype):
    sigPriceBuy = []
    sigPriceSell = []
    flag = -1
    
    for i in range(len(data)):
        if data['macd'][i] < data['signal'][i] :
            if flag != 1:
                sigPriceBuy.append(data[pricetype][i])
                sigPriceSell.append(npnan)
                flag = 1
            else:
                sigPriceBuy.append(npnan)
                sigPriceSell.append(npnan)
        elif data['macd'][i] > data['signal'][i] :
             if flag != 0:
                sigPriceBuy.append(npnan)
                sigPriceSell.append(data[pricetype][i])
                flag = 0
             else:
                sigPriceBuy.append(npnan)
                sigPriceSell.append(npnan)
        else:
                sigPriceBuy.append(npnan)
                sigPriceSell.append(npnan)
    data['sigPriceBuy'] = sigPriceBuy
    data['sigPriceSell'] = sigPriceSell
    return data #(sigPriceBuy, sigPriceSell)


def plotChart(df, name, pricetype):
    start = 0;
    end = len(df);
    #Visualize the data
    
    fig, axs = plt.subplots(3, figsize=(20, 10))
    fig.suptitle(compname + ' Stock - ' + name)
    axs[0].plot(df[pricetype][start:end], label = pricetype + ' Price', linewidth=1, color='blue')
    axs[0].scatter(df.index[start:end], df['sigPriceBuy'][start:end], label = 'buy', marker= '^', color='green')
    axs[0].scatter(df.index[start:end], df['sigPriceSell'][start:end], label = 'sell', marker= 'v', color='red')
    
    axs[1].plot(df['macd'][start:end], label = 'macd', linewidth=1, color='green')
    axs[1].plot(df['signal'][start:end], label = 'signal', linewidth=1, color='red')
    
    axs[2].bar(df.index[start:end], df['histogram'][start:end], label = 'histogram')
    fig.legend()
    fig.savefig(name +'.png')
    fig.show()    
    return 0

def calcHLOCV(df, sample):
    dfH = df.resample(sample).max()
    dfL = df.resample(sample).min()
    dfO = df.resample(sample).first()
    dfC = df.resample(sample).last()
    dfV = df.resample(sample).sum()
    
    PVList=[]
    for row in range(len(dfH)):
        if(not math.isnan(dfH['value'][row])) :
            PV = [dfH.index[row], dfH['value'][row], dfL['value'][row], dfO['value'][row], dfC['value'][row] , dfV['volume'][row]]
            PVList.append(PV)    
    return pd.DataFrame(PVList, columns =['date', 'high', 'low', 'open', 'close', 'volume'])

#Logic
df = caculate_macd(df, 'value')
df = buy_sell(df, 'value')
plotChart(df, '1T', 'value')

df['datestr'] = df['date']
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d-%H-%M')
df.set_index('date', inplace = True)

df3 = calcHLOCV(df, '3T');
df3 = caculate_macd(df3, 'close')
df3 = buy_sell(df3, 'close')
plotChart( df3, '3T', 'close')

df5 = calcHLOCV(df, '5T');
df5 = caculate_macd(df5, 'close')
df5 = buy_sell(df5, 'close')
plotChart( df5, '5T', 'close')

df10 = calcHLOCV(df, '10T');
df10 = caculate_macd(df10, 'close')
df10 = buy_sell(df10, 'close')
plotChart( df10, '10T', 'close')

df15 = calcHLOCV(df, '15T');
df15 = caculate_macd(df15, 'close')
df15 = buy_sell(df15, 'close')
plotChart( df15, '15T', 'close')

      
FinalList = [];

## All
#for i in range(len(df)):
#    datetime = str(df.index[i])
#    resultDict = { '1T': df.iloc[1].to_frame().to_json() }
#    d3 = df3.query('date == "'+datetime+'"')
#    if(len(d3) == 1):
#        resultDict['3T'] = d3.to_json()       
#    d5 = df5.query('date == "'+datetime+'"')
#    if(len(d5) == 1):
#        resultDict['5T'] = d5.to_json() #str(d5.to_json(orient='records', lines=True))   
#    d10 = df10.query('date == "'+datetime+'"')
#    if(len(d10) == 1):
#        resultDict['10T'] = d10.to_json()       
#    d15 = df15.query('date == "'+datetime+'"')
#    if(len(d15) == 1):
#        resultDict['15T'] = d15.to_json()

### Short
#for i in range(len(df)):
#    datetime = str(df.index[i])
#    resultDict = { 'value': df.iloc[i]['value'],  'date': datetime}
#    d3 = df3.query('date == "'+datetime+'"')
#    if(len(d3) == 1):
#        resultDict['3T'] = { 'sell': d3.iloc[0]['sigPriceSell'] , 'buy': d3.iloc[0]['sigPriceBuy']}
#    d5 = df5.query('date == "'+datetime+'"')
#    if(len(d5) == 1):
#        resultDict['5T'] = { 'sell': d5.iloc[0]['sigPriceSell'] , 'buy': d5.iloc[0]['sigPriceBuy']}
#    d10 = df10.query('date == "'+datetime+'"')
#    if(len(d10) == 1):
#        resultDict['10T'] = { 'sell': d10.iloc[0]['sigPriceSell'] , 'buy': d10.iloc[0]['sigPriceBuy']} 
#    d15 = df15.query('date == "'+datetime+'"')
#    if(len(d15) == 1):
#        resultDict['15T'] = { 'sell': d15.iloc[0]['sigPriceSell'] , 'buy': d15.iloc[0]['sigPriceBuy']}

## Short object only
#for i in range(len(df)):
#    datetime = str(df.index[i])
#    resultDict = { 'index' : i, 'value': df.iloc[i]['value'],  'date': datetime}
#    d3 = df3.query('date == "'+datetime+'"')
#    if(len(d3) == 1):
#        resultDict['3T_sell'] = d3.iloc[0]['sigPriceSell']
#        resultDict['3T_buy'] = d3.iloc[0]['sigPriceBuy']
#    d5 = df5.query('date == "'+datetime+'"')
#    if(len(d5) == 1):
#        resultDict['5T_sell'] = d5.iloc[0]['sigPriceSell'] 
#        resultDict['5T_buy'] = d5.iloc[0]['sigPriceBuy']
#    d10 = df10.query('date == "'+datetime+'"')
#    if(len(d10) == 1):
#        resultDict['10T_sell'] = d10.iloc[0]['sigPriceSell'] 
#        resultDict['10T_buy'] = d10.iloc[0]['sigPriceBuy']
#    d15 = df15.query('date == "'+datetime+'"')
#    if(len(d15) == 1):
#        resultDict['15T_sell'] = d15.iloc[0]['sigPriceSell'] 
#        resultDict['15T_buy'] = d15.iloc[0]['sigPriceBuy']

## Plot
for i in range(len(df)):
    datetime = str(df.index[i])
    d3 = df3.query('date == "'+datetime+'"')
    T3_sell = np.nan
    T3_buy = np.nan
    T5_sell = np.nan
    T5_buy = np.nan
    T10_sell = np.nan
    T10_buy = np.nan
    T15_sell = np.nan
    T15_buy = np.nan
    if(len(d3) == 1):
        T3_sell = d3.iloc[0]['sigPriceSell']
        T3_buy = d3.iloc[0]['sigPriceBuy']
    d5 = df5.query('date == "'+datetime+'"')
    if(len(d5) == 1):
        T5_sell = d5.iloc[0]['sigPriceSell'] 
        T5_buy = d5.iloc[0]['sigPriceBuy']
    d10 = df10.query('date == "'+datetime+'"')
    if(len(d10) == 1):
        T10_sell = d10.iloc[0]['sigPriceSell'] 
        T10_buy = d10.iloc[0]['sigPriceBuy']
    d15 = df15.query('date == "'+datetime+'"')
    if(len(d15) == 1):
        T15_sell = d15.iloc[0]['sigPriceSell'] 
        T15_buy = d15.iloc[0]['sigPriceBuy']
    resultDict = [ i,  df.iloc[i]['value'], datetime, T3_sell ,T3_buy , T5_sell ,T5_buy , T10_sell , T10_buy ,T15_sell ,T15_buy ]
    FinalList.append(resultDict)
dffinal = pd.DataFrame(FinalList, columns =['index', 'value', 'datetime', 'T3_sell' ,'T3_buy' , 'T5_sell' ,'T5_buy' , 'T10_sell' , 'T10_buy' ,'T15_sell' ,'T15_buy'])    

# Writing to json file
with open(compname + '.json', 'w') as outfile: 
    outfile.write(str(json.dumps(FinalList)).replace("NaN", '0'))
    
fig, axs = plt.subplots(4, figsize=(20, 10))
fig.suptitle(compname + ' Stock')
start = 1500;
end = len(df);

axs[0].plot(dffinal['value'][start:end], label = 'price T3', linewidth=1, color='lime')
axs[0].scatter(dffinal.index[start:end], dffinal['T3_buy'][start:end], label = 'T3_buy', marker= '^', color='green')
axs[0].scatter(dffinal.index[start:end], dffinal['T3_sell'][start:end], label = 'T3_sell', marker= 'v', color='red')

axs[1].plot(dffinal['value'][start:end], label = 'price T5', linewidth=1, color='blue')
axs[1].scatter(dffinal.index[start:end], dffinal['T5_buy'][start:end], label = 'T5_buy', marker= '^', color='green')
axs[1].scatter(dffinal.index[start:end], dffinal['T5_sell'][start:end], label = 'T5_sell', marker= 'v', color='red')

axs[2].plot(dffinal['value'][start:end], label = 'price T10', linewidth=1, color='yellow')
axs[2].scatter(dffinal.index[start:end], dffinal['T10_buy'][start:end], label = 'T5_buy', marker= '^', color='green')
axs[2].scatter(dffinal.index[start:end], dffinal['T10_sell'][start:end], label = 'T5_sell', marker= 'v', color='red')

axs[3].plot(dffinal['value'][start:end], label = 'price T15', linewidth=1, color='pink')
axs[3].scatter(dffinal.index[start:end], dffinal['T15_buy'][start:end], label = 'T5_buy', marker= '^', color='green')
axs[3].scatter(dffinal.index[start:end], dffinal['T15_sell'][start:end], label = 'T5_sell', marker= 'v', color='red')


fig.legend()
fig.savefig(compname +'_decision.png')
fig.show()    
