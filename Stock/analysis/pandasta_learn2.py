# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 16:20:29 2021

@author: Pritam

https://pypi.org/project/ta/
pip install ta

https://technical-analysis-library-in-python.readthedocs.io/en/latest/

https://github.com/bukosabino/ta
https://towardsdatascience.com/trading-strategy-technical-analysis-with-python-ta-lib-3ce9d6ce5614

https://towardsdatascience.com/technical-analysis-library-to-financial-datasets-with-pandas-python-4b2b390d3543

http://theautomatic.net/2021/02/02/technical-analysis-with-python/
"""
import os
import math
import numpy as np
import pandas as pd
import json

from ta import add_all_ta_features
from ta.utils import dropna
from ta.volatility import BollingerBands
from ta.momentum import RSIIndicator
from ta.trend import macd

fname = 'TCS'

df = pd.DataFrame(json.load(open('data/D/'+ fname +'.json')))

# Clean NaN values
df = dropna(df)

# or remove NaN values
# df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].replace(np.nan, 0)
# df = df[df['close'] > 0]

 # SMA
def sma(df):
    df['SMA5'] = df['close'].rolling(window=5).mean()
    df['SMA10'] = df['close'].rolling(window=10).mean()
    df['SMA20'] = df['close'].rolling(window=20).mean()
    df['SMA50'] = df['close'].rolling(window=50).mean()
    df['SMA100'] = df['close'].rolling(window=100).mean()
    df['SMA200'] = df['close'].rolling(window=200).mean()
    
    df['SMA_CO_5_20'] = df['SMA5'] > df['SMA20']
    df['SMA_CO_20_50'] = df['SMA20'] > df['SMA50']
    df['SMA_CO_50_200'] = df['SMA50'] > df['SMA200'] 
    return df

# EMA
def ema(df):
    df['EMA5'] = df['close'].ewm(span=5, adjust=False).mean()
    df['EMA10'] = df['close'].ewm(span=10, adjust=False).mean()
    df['EMA20'] = df['close'].ewm(span=20, adjust=False).mean()
    df['EMA50'] = df['close'].ewm(span=50, adjust=False).mean()
    df['EMA100'] = df['close'].ewm(span=100, adjust=False).mean()
    df['EMA200'] = df['close'].ewm(span=200, adjust=False).mean()
    
    df['EMA_CO_5_20'] = df['EMA5'] > df['EMA20']
    df['EMA_CO_20_50'] = df['EMA20'] > df['EMA50']
    df['EMA_CO_50_200'] = df['EMA50'] > df['EMA200'] 
    return df


print(df.columns)

# for y in df.columns:
#     print(y, type(y))
# print(df.head())


# change string to Date
# df.reset_index(inplace = True)
# df['index'] = df['index'].str[0:10]
# df['index'] = df['index'].apply(lambda x: datetime.fromtimestamp(int(x)))

# # df = df.drop(df[df['open'] == 0].index, inplace = True)
# # dfFiter = df[df['open'] > 0]'=

# df['open'] = df['open'].apply(lambda x: float(x))
# # df['datetime'] = df['datetime'].astype('datetime64[ns]')
