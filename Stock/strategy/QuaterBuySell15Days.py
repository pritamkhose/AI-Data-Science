# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 21:21:41 2021

@author: Pritam

https://stackoverflow.com/questions/20638006/convert-list-of-dictionaries-to-a-pandas-dataframe
https://www.geeksforgeeks.org/python-pandas-dataframe-resample/

"""
#Import the libraries
import os
import math
import numpy as np
import pandas as pd
import json
import requests


compname = 'W'

url = 'https://www.moneycontrol.com/mc/widget/basicchart/get_chart_value?classic=true&dur=max&sc_did=' + compname
datajson = requests.get(url).json()
df = pd.DataFrame(datajson['g1'])

df = df.drop(['value'], axis = 1) 
df[['high', 'low','open', 'close', 'volume']] = df[['high', 'low','open', 'close', 'volume']].astype(float)
df.to_json(compname + '.json', orient='records')

# Read json file in folder  
with open(compname + '.json') as json_file:
    dataread = json.load(json_file)   
df = pd.DataFrame(dataread)

df['datestr'] = df['date']
df['P'] = (df['high'] + df['low']+ df['close'])/3
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
df.set_index('date', inplace = True) 

def calcHLOCV(df, sample):
    dfH = df.high.resample(sample).max().to_frame() 
    dfL = df.low.resample(sample).min().to_frame() 
    dfO = df.open.resample(sample).first().to_frame() 
    dfC = df.close.resample(sample).last().to_frame() 
    dfP = df.P.resample(sample).mean().to_frame() 
    dfV = df.volume.resample(sample).sum().to_frame() 
    
    PVList=[]
    for row in range(len(dfH)):
        PV = [dfH.index[row], dfH['high'][row], dfL['low'][row], dfO['open'][row], dfC['close'][row], dfP['P'][row], dfV['volume'][row]]
        PVList.append(PV)    
    return pd.DataFrame(PVList, columns =['date', 'high', 'low', 'open', 'close', 'P', 'volume'])

    
# dfW = calcHLOCV(df, 'W');
dfSM = calcHLOCV(df, 'SM');
# dfM = calcHLOCV(df, 'M');
# dfQ = calcHLOCV(df, 'Q');

dfSM['HH'] = dfSM['high'].rolling(window=2).max()
dfSM['LL'] = dfSM['low'].rolling(window=2).min()
dfSM['diff'] = dfSM['HH'] - dfSM['LL']
dfSM['cp1'] = dfSM['close'] - dfSM['close'].shift(1)
dfSM['cp2'] = dfSM['close'] - dfSM['close'].shift(2)
dfSM['cp3'] = dfSM['close'] - dfSM['close'].shift(3)
dfSM['cp4'] = dfSM['close'] - dfSM['close'].shift(4)
dfSM['cp5'] = dfSM['close'] - dfSM['close'].shift(5)

dfSM['datestr'] = np.datetime_as_string(dfSM['date'], unit='D')

dfSM['qtr'] = dfSM['datestr'].str.contains("-01-15|-04-15|-07-15|-10-15")
dfSM['cp1'] = dfSM['qtr'] * dfSM['cp1']
dfSM['cp2'] = dfSM['qtr'] * dfSM['cp2']
dfSM['cp3'] = dfSM['qtr'] * dfSM['cp3']
dfSM['cp4'] = dfSM['qtr'] * dfSM['cp4']
dfSM['cp5'] = dfSM['qtr'] * dfSM['cp5']
