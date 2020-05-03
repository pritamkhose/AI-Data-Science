# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 19:02:04 2020

@author: Pritam

https://school.stockcharts.com/doku.php?id=technical_indicators:average_directional_index_adx
https://www.investopedia.com/terms/a/adx.asp

https://school.stockcharts.com/doku.php?id=technical_indicators:average_true_range_atr

https://school.stockcharts.com/doku.php?id=technical_indicators:williams_r

https://school.stockcharts.com/doku.php?id=technical_indicators:money_flow_index_mfi

https://school.stockcharts.com/doku.php?id=technical_indicators:commodity_channel_index_cci

https://school.stockcharts.com/doku.php?id=technical_indicators:rate_of_change_roc_and_momentum

https://school.stockcharts.com/doku.php?id=technical_indicators:bollinger_bands


"""

#Import the libraries
import math
import pandas_datareader as web
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

#Get the stock quote
df = web.DataReader('INFY.NS', data_source='yahoo', start='2019-01-01', end='2020-05-02')

df['HL'] = df['High'] - df['Low']
df['HpC'] = abs(df['High'].shift(1) - df['Close'])
df['LpC'] = abs(df['Low'].shift(1) - df['Close'])
df['TR'] = df[['HL', 'HpC', 'LpC']].max(axis=1)

df['zeros'] = 0
df['HHp'] = df['High'] - df['High'].shift(1)
df['LpL'] = df['Low'].shift(1) - df['Low']

df['HHp0'] = df[['HHp', 'zeros']].max(axis=1)
df['LpL0'] = df[['LpL', 'zeros']].max(axis=1)
df['DM1+'] = np.where(df['HHp'] > df['LpL'], df['HHp0'], 0)
df['DM1-'] = np.where(df['LpL'] > df['HHp'], df['LpL0'], 0)

df['TR14'] = df.iloc[:,9].rolling(window=14).mean()  #df['TR']
df['DM14+'] = df.iloc[:,15].rolling(window=14).mean()  #df['DM1+']
df['DM14-'] = df.iloc[:,16].rolling(window=14).mean()  #df['DM1-']
df['DI14+'] = (100*(df['DM14+']/df['TR14']))
df['DI14-'] = (100*(df['DM14-']/df['TR14']))
df['DI14Diff'] = abs(df['DI14+'] - df['DI14-'])
df['DI14Sum'] = df['DI14+'] + df['DI14-']
df['DX'] = (100*(df['DI14Diff']/df['DI14Sum']))
df['ADX'] = df.iloc[:,24].rolling(window=14).mean() #df['DX']

#df['HCp'] = abs(df['High'] - df['Close'].shift(1))
#df['LCp'] = abs(df['Low'] - df['Close'].shift(1))
#df['TR_ATR'] = df[['HCp', 'LCp']].max(axis=1)
#df['ATR'] = df.iloc[:,28].rolling(window=14).mean()  #df['TR_ATR']

#Visualize the data
plt.figure(figsize=(16,8))
plt.title('Stock')
plt.xlabel('Date', fontsize=10)
plt.plot(df['ADX'], linewidth=1)
plt.legend(['ADX'], loc='lower right')
#plt.show()
plt.savefig('1.png')