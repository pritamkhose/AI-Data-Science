# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 12:47:06 2020

@author: Pritam

https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.resample.html

TimeFrame - 30S - 30 second, 5T or 5min- 5 minute, M, W, Q, A
"""

import requests
import os
import math
import numpy as np
import pandas as pd
import pandas_ta as ta
import json
from datetime import datetime

fname = 'TCS'

folderList = ['data', 'data/5T/', 'data/15T/', 'data/30T/','data/D/', 'data/W/', 'data/M/']
for x in folderList:
    try:
        if not os.path.exists(x):
            os.makedirs(x)
    except OSError as err:
        print(err)


def readCSV(fname):
    df = pd.read_csv('data/'+fname+'.csv')
    df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].replace(np.nan, 0)
    df = df[df['open'] > 0]
    # df.reset_index(inplace = False)
    # for y in df.columns:
    #     print(y, type(y))
    # print(df.head())
    # print(df.columns)
    # print(df.info())
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

def calcHLOCV(dftemp, sample):
    dfH = dftemp.high.resample(sample).max().to_frame() 
    dfL = dftemp.low.resample(sample).min().to_frame() 
    dfO = dftemp.open.resample(sample).first().to_frame() 
    dfC = dftemp.close.resample(sample).last().to_frame() 
    dfV = dftemp.volume.resample(sample).sum().to_frame() 
    
    PVList=[]
    for row in range(len(dfH)):
        if(dfV['volume'][row] != 0):
            PV = [dfH.index[row], dfH['high'][row], dfL['low'][row], dfO['open'][row], dfC['close'][row], dfV['volume'][row]]
            PVList.append(PV)
    dftemp = pd.DataFrame(PVList, columns =['timestamp', 'high', 'low', 'open', 'close', 'volume'])
    # dftemp.set_index('timestamp', inplace = True)
    dftemp.to_json('data/'+sample+'/'+ fname +'.json')
    return dftemp

df = readCSV(fname)
df.set_index('timestamp', inplace = True)
# df = df.loc[((df['timestamp'] > '2017-01-01') & (df['timestamp'] <= '2017-01-31'))]

dfD = calcHLOCV(df, 'D')
dfW = calcHLOCV(df, 'W')
dfM = calcHLOCV(df, 'M')

df5T = calcHLOCV(df, '5T')
df15T = calcHLOCV(df, '15T')
df30T = calcHLOCV(df, '30T')

dfD = pd.DataFrame(json.load(open('data/D/'+ fname +'.json')))
dfW = pd.DataFrame(json.load(open('data/W/'+ fname +'.json')))
dfM = pd.DataFrame(json.load(open('data/M/'+ fname +'.json')))