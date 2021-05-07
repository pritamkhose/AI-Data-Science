# -*- coding: utf-8 -*-
"""
Created on Tue May  4 22:32:39 2021

@author: Pritam

# https://www.investopedia.com/articles/trading/07/adx-trend-indicator.asp
# https://www.investopedia.com/articles/active-trading/031914/how-traders-can-utilize-cci-commodity-channel-index-trade-stock-trends.asp
# https://www.investopedia.com/terms/m/mfi.asp

"""

from datetime import datetime
import os
import numpy as np
import pandas as pd
import json

dirPath = 'E:/Code/python/AIDataScience/Stock/moneycontrol/data/techD/'


def getData():
    data = []
    for path, subdirs, files in os.walk(dirPath):
        for name in files:
            if ".rar" in name:
                continue
            else:
                data.append(os.path.join(path, name))
    return data


# fileList = getData()

df = pd.DataFrame(json.load(open(dirPath + 'W'+ '.json')))
# print(df.columns)

 # take last 5Y or min days
dflen = len(df)
df = df[dflen-330:dflen]

#df.iloc[3] # df.loc[3]  'close',
dfData = df[['d_rsi','d_stochrsi', 'd_stoch_d', 'd_fsto', 'd_ao', 'd_williams_r', 'd_roc',
       'd_macd', 'd_adx', 'd_cci', 'd_mfi', 'd_vwamp', 'd_ma']] 

dfDataShift = dfData.shift(1)
dfDecsion = dfData == dfDataShift
dfDecsion = dfDecsion.replace({True: 0, False: 1})

dfDecsion = dfDecsion * dfDataShift
dfDecsion = dfDecsion.replace({-0: 0, np.nan: 0})
dfDecsion['time'] = df['time']
dfDecsion['sum'] = dfDecsion.sum(axis=1)

col = ['rsi','stochrsi', 'stoch_d','stochrsi_d', 'stochrsi_k', 'stoch_fsto', 'ao', 'williams_r', 'roc', 'macd', 'macd_signal', 'macd_diff', 'adx', 'cci', 'mfi', 'vwamp']
dfDecsion[col] = df[col] 

dfDecsionShort = dfDecsion[['time', 'sum', 'rsi', 'd_rsi', 'stochrsi', 'stochrsi_d', 'stochrsi_k', 'd_stochrsi', 'macd', 'macd_signal', 'macd_diff', 'd_macd']]

## dfDecsion = dfDecsion[dfDecsion['sum'] != 0]
# dfDecsion_rsi = dfDecsion[['time', 'd_rsi']] #, 'sum'
# dfDecsion_rsi['rsi'] = df['rsi'] 
# dfDecsion_rsi_select = dfDecsion_rsi[dfDecsion_rsi['d_rsi'] != 0]

# dd = df[['time', 'rsi', 'd_rsi',]]
# dd['change'] = dfDecsion_rsi['d_rsi']
## dd = dd[dd['d_rsi'] != 0]