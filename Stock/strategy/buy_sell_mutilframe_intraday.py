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
compname = 'IT'
#url = 'https://www.moneycontrol.com/mc/widget/basicchart/get_chart_value?classic=true&dur=max&sc_did=' + compname
url = 'https://www.moneycontrol.com/mc/widget/basicchart/get_chart_value?classic=true&dur=5d&sc_did=' + compname
#url = 'http://ec2-13-59-211-101.us-east-2.compute.amazonaws.com:3000/daily/'+ compname
datajson = requests.get(url).json()
stock = datajson['g1']
PVList = [];
for row in range(len(stock)):
#    PVList.append([pd.to_datetime(stock[row]['date']), float(stock[row]['value']), float(stock[row]['volume'])])
    PVList.append([stock[row]['date'], float(stock[row]['value']), float(stock[row]['volume'])])
df = pd.DataFrame(PVList ,columns =['date', 'value', 'volume']) 

decimalpoint = 2

# Function
def caculate_macd(df, pricetype):
    df_EMA_9 = df[pricetype].ewm(span=9,adjust=False).mean()
    df_EMA_12 = df[pricetype].ewm(span=12,adjust=False).mean()
    df_EMA_26 = df[pricetype].ewm(span=26,adjust=False).mean()
        
    df['macd'] = df_EMA_12 - df_EMA_26
    df['signal'] = df['macd']*(2/(df_EMA_9+1))+df['macd'].shift(-1)*(1-(2/(df_EMA_9+1)))
    df['histogram'] =  df['macd'] - df['signal']
    return df


def caculate_mov(df, pricetype):
    df_ema5 = df[pricetype].ewm(span=5,adjust=False).mean()
    df_ema10 = df[pricetype].ewm(span=10,adjust=False).mean()
    df_ema20 = df[pricetype].ewm(span=20,adjust=False).mean()
    df_ema50 = df[pricetype].ewm(span=50,adjust=False).mean()
    df['EMA_avg'] = 50 + 5*(np.where(df_ema5 > df_ema10, 1, -1) + np.where( df_ema10 > df_ema20, 2, -2) + np.where(df_ema20 > df_ema50, 3, -3))
    
    df_sma5 = df[pricetype].rolling(window=5).mean()
    df_sma10 = df[pricetype].rolling(window=10).mean()
    df_sma20 = df[pricetype].rolling(window=20).mean()
    df_sma50 = df[pricetype].rolling(window=30).mean()
    df['SMA_avg'] = 50 + 5*(np.where(df_sma5 > df_sma10, 1, -1) + np.where( df_sma10 > df_sma20, 2, -2) + np.where(df_sma20 > df_sma50, 3, -3))
    return df


def cal_Bollinger_Bands(df, pricetype):
    # Bollinger band
    window = 20
    no_of_std = 2
    df['BollingerMean']  = df['close'].rolling(window).mean()
    rolling_std = df['close'].rolling(window).std()
    #create two new DataFrame columns to hold values of upper and lower Bollinger bands
    df['BollingerHigh'] = df['BollingerMean'] + (rolling_std * no_of_std)
    df['BollingerLow'] = df['BollingerMean'] - (rolling_std * no_of_std)
    return df
    
def rsi_ud(df_diff):
    PVList=[]
    for row in range(len(df_diff)):
        if(row == 0):
            U = 0
            D = 0
        elif(df_diff[row] < 0):
            U = 0
            D = df_diff[row] * -1
        else:
            U = df_diff[row]
            D = 0
        PVList.append([df_diff[row], U, D])   
    return pd.DataFrame(PVList, columns =['diff', 'U', 'D']);

def caculate_rsi(df, pricetype):
    df_diff =  rsi_ud(df[pricetype].diff())
    rsiday = 14
    aList=[]
    for row in range(len(df)):
        smau = df_diff['U'][row-(rsiday):row+1].mean()
        smad = df_diff['D'][row-(rsiday):row+1].mean()
        aList.append(100/(1+(smau/smad)))
    df['rsi'] = pd.DataFrame(aList, columns =['rsi'])   
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
    
    fig, axs = plt.subplots(4, figsize=(20, 10))
    fig.suptitle(compname + ' Stock - ' + name)
    axs[0].plot(df[pricetype][start:end], label = pricetype + ' Price', linewidth=1, color='blue')
    axs[0].scatter(df.index[start:end], df['sigPriceBuy'][start:end], label = 'buy', marker= '^', color='green')
    axs[0].scatter(df.index[start:end], df['sigPriceSell'][start:end], label = 'sell', marker= 'v', color='red')
    
    axs[1].plot(df['macd'][start:end], label = 'macd', linewidth=1, color='green')
    axs[1].plot(df['signal'][start:end], label = 'signal', linewidth=1, color='red')
    axs[1].bar(df.index[start:end], df['histogram'][start:end], label = 'histogram')
    
    axs[2].plot(df['rsi'][start:end], label = 'RSI', linewidth=1, color='red')
    axs[2].plot(df['EMA_avg'][start:end], label = 'EMA avg', linewidth=1, color='blue')
    axs[2].plot(df['SMA_avg'][start:end], label = 'SMA avg', linewidth=1, color='green')
    
#    axs[3].bar(df.index[start:end], df['volume'][start:end], label = 'volume')
    axs[3].plot(df[pricetype][start:end], label = pricetype + ' Price', linewidth=1, color='blue')
    axs[3].plot(df['BollingerHigh'][start:end], label = 'high', linewidth=1, color='green')
    axs[3].plot(df['BollingerLow'][start:end], label = 'low', linewidth=1, color='red')
    axs[3].plot(df['BollingerMean'][start:end], label = 'mean', linewidth=1, color='black')
    
    
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
#plotChart(df, '1T', 'value')

df['datestr'] = df['date']
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d-%H-%M')
df.set_index('date', inplace = True)

df3 = calcHLOCV(df, '3T');
df3 = caculate_macd(df3, 'close')
df3 = caculate_rsi(df3, 'close')
df3 = caculate_mov(df3, 'close')
df3 = cal_Bollinger_Bands(df3, 'close')
df3 = buy_sell(df3, 'close')
plotChart( df3, '3T', 'close')

df5 = calcHLOCV(df, '5T');
df5 = caculate_macd(df5, 'close')
df5 = caculate_rsi(df5, 'close')
df5 = caculate_mov(df5, 'close')
df5 = cal_Bollinger_Bands(df5, 'close')
df5 = buy_sell(df5, 'close')
plotChart( df5, '5T', 'close')

df10 = calcHLOCV(df, '10T');
df10 = caculate_macd(df10, 'close')
df10 = caculate_rsi(df10, 'close')
df10 = caculate_mov(df10, 'close')
df10 = cal_Bollinger_Bands(df10, 'close')
df10 = buy_sell(df10, 'close')
plotChart( df10, '10T', 'close')

df15 = calcHLOCV(df, '15T');
df15 = caculate_macd(df15, 'close')
df15 = caculate_rsi(df15, 'close')
df15 = caculate_mov(df15, 'close')
df15 = cal_Bollinger_Bands(df15, 'close')
df15 = buy_sell(df15, 'close')
plotChart( df15, '15T', 'close')

      
FinalList = [];

## Plot
for i in range(len(df)):
    datetime = str(df.index[i])
    d3 = df3.query('date == "'+datetime+'"')
    MACD_T3_sell = np.nan
    MACD_T3_buy = np.nan
    MACD_T5_sell = np.nan
    MACD_T5_buy = np.nan
    MACD_T10_sell = np.nan
    MACD_T10_buy = np.nan
    MACD_T15_sell = np.nan
    MACD_T15_buy = np.nan
    if(len(d3) == 1):
        MACD_T3_sell = d3.iloc[0]['sigPriceSell']
        MACD_T3_buy = d3.iloc[0]['sigPriceBuy']
        RSI_T3_buy = d3.iloc[0]['sigPriceBuy']
    d5 = df5.query('date == "'+datetime+'"')
    if(len(d5) == 1):
        MACD_T5_sell = d5.iloc[0]['sigPriceSell'] 
        MACD_T5_buy = d5.iloc[0]['sigPriceBuy']
    d10 = df10.query('date == "'+datetime+'"')
    if(len(d10) == 1):
        MACD_T10_sell = d10.iloc[0]['sigPriceSell'] 
        MACD_T10_buy = d10.iloc[0]['sigPriceBuy']
    d15 = df15.query('date == "'+datetime+'"')
    if(len(d15) == 1):
        MACD_T15_sell = d15.iloc[0]['sigPriceSell'] 
        MACD_T15_buy = d15.iloc[0]['sigPriceBuy']
    resultDict = [ i,  df.iloc[i]['value'], datetime, MACD_T3_sell ,MACD_T3_buy , MACD_T5_sell ,MACD_T5_buy , MACD_T10_sell , MACD_T10_buy ,MACD_T15_sell ,MACD_T15_buy ]
    FinalList.append(resultDict)
dffinal = pd.DataFrame(FinalList, columns =['index', 'value', 'datetime', 'MACD_T3_sell' ,'MACD_T3_buy' , 'MACD_T5_sell' ,'MACD_T5_buy' , 'MACD_T10_sell' , 'MACD_T10_buy' ,'MACD_T15_sell' ,'MACD_T15_buy'])    

# Writing to json file
with open(compname + '.json', 'w') as outfile: 
    outfile.write(str(json.dumps(FinalList)).replace("NaN", '0'))
    
fig, axs = plt.subplots(4, figsize=(20, 10))
fig.suptitle(compname + ' Stock')
start = 1000;
end = len(df);

axs[0].plot(dffinal['value'][start:end], label = 'price T3', linewidth=1, color='lime')
axs[0].scatter(dffinal.index[start:end], dffinal['MACD_T3_buy'][start:end], label = 'T3_buy', marker= '^', color='green')
axs[0].scatter(dffinal.index[start:end], dffinal['MACD_T3_sell'][start:end], label = 'T3_sell', marker= 'v', color='red')

axs[1].plot(dffinal['value'][start:end], label = 'price T5', linewidth=1, color='blue')
axs[1].scatter(dffinal.index[start:end], dffinal['MACD_T5_buy'][start:end], label = 'T5_buy', marker= '^', color='green')
axs[1].scatter(dffinal.index[start:end], dffinal['MACD_T5_sell'][start:end], label = 'T5_sell', marker= 'v', color='red')

axs[2].plot(dffinal['value'][start:end], label = 'price T10', linewidth=1, color='yellow')
axs[2].scatter(dffinal.index[start:end], dffinal['MACD_T10_buy'][start:end], label = 'T10_buy', marker= '^', color='green')
axs[2].scatter(dffinal.index[start:end], dffinal['MACD_T10_sell'][start:end], label = 'T10_sell', marker= 'v', color='red')

axs[3].plot(dffinal['value'][start:end], label = 'price T15', linewidth=1, color='pink')
axs[3].scatter(dffinal.index[start:end], dffinal['MACD_T15_buy'][start:end], label = 'T15_buy', marker= '^', color='green')
axs[3].scatter(dffinal.index[start:end], dffinal['MACD_T15_sell'][start:end], label = 'T15_sell', marker= 'v', color='red')


fig.legend()
fig.savefig(compname +'_decision.png')
fig.show()    
