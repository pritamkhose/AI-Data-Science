# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 12:47:06 2020

@author: Pritam

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
def readCSV():
    df = pd.read_csv('data/'+fname+'.csv')
    df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].replace(np.nan, 0)
    df = df[df['open'] > 0]
    df.reset_index(inplace = False)
    # for y in df.columns:
    #     print(y, type(y))
    # print(df.head())
    # print(df.info())
    df['timestamp'] = pd.to_datetime(df['timestamp'])


# df = df.loc[((df['timestamp'] > '2017-01-01') & (df['timestamp'] <= '2017-01-31'))]

def calcHLOCV(dftemp, sample):
    dftemp.set_index('timestamp', inplace = True)
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
    dftemp.to_json('data/'+sample+'/'+ fname +'.json')
    return dftemp

# dfD = calcHLOCV(df, 'D')
dfD = pd.DataFrame(json.load(open('data/D/'+ fname +'.json')))
# dfD.set_index('timestamp', inplace = True)

dfD['logR'] = dfD.ta.log_return(cumulative=True, append=True)
dfD['percentR'] = dfD.ta.percent_return(cumulative=True, append=True)
dfD['sma10'] = ta.sma(dfD.close, length=10)

print(dfD.columns)
# print(dfD.ta.indicators())
