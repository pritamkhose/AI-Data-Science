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
https://www.geeksforgeeks.org/python-pandas-series-mad-to-calculate-mean-absolute-deviation-of-a-series/

https://school.stockcharts.com/doku.php?id=technical_indicators:rate_of_change_roc_and_momentum

https://school.stockcharts.com/doku.php?id=technical_indicators:bollinger_bands
https://www.pythonforfinance.net/2017/07/31/bollinger-band-trading-strategy-backtest-in-python/

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

df['HCp'] = abs(df['High'] - df['Close'].shift(1))
df['LCp'] = abs(df['Low'] - df['Close'].shift(1))
df['TR_ATR'] = df[['HCp', 'LCp']].max(axis=1)
df['ATR'] = df.iloc[:,8].rolling(window=14).mean()  #df['TR_ATR']

df['P'] = (df['High'] + df['Low'] + df['Close'])/3
df['UD'] = np.where(df['P'] > df['P'].shift(1), 1, -1)
df['RawMoneyFlow'] = df['P'] * df['Volume']
df['DM1+'] = np.where(df['UD'] > 0, df['RawMoneyFlow'], 0)
df['DM1-'] = np.where(df['UD'] < 0, df['RawMoneyFlow'], 0)

df['DM14+'] = df.iloc[:,13].rolling(window=14).mean()
df['DM14-'] = df.iloc[:,14].rolling(window=14).mean()
df['Ratio'] = df['DM14+'] / df['DM14-']
df['MFI'] = 100 - (100/(1+df['Ratio']))

df['HH14'] = df.iloc[:,0].rolling(window=14).max()
df['LL14'] = df.iloc[:,1].rolling(window=14).min()
df['Williamson'] =  ((df['HH14']- df['Close'])/(df['HH14']- df['LL14'])) * (-100)

df['ROC'] = ((df['Close']- df['Close'].shift(20))/df['Close'].shift(20))*100


df['SMA20P'] = df.iloc[:,10].rolling(window=20).mean()
#list_of_values = []
#df.iloc[:,10].rolling(window=20).apply(lambda x: list_of_values.append(x.values) or 0, raw=False)
##df['dSMA20Plist']
#PVList = []
#for row in range(len(list_of_values)):
#    dev = pd.Series(list_of_values[row]).mad()
#    PV = [df.index[row], dev]
#    PVList.append(PV)    
#df1 = pd.DataFrame(PVList, columns =['index', 'dev']) 
##dffinal = df1.join(df, on='index', how='inner')
#df['CCI'] =(df['P']-df['SMA20P'])/(0.015*df1['dev'])

df['dev'] = df['SMA20P'].rolling(window).std()
df['CCI'] = (df['P']-df['SMA20P'])/(0.015*df['dev'])

# Bollinger band
window = 20
no_of_std = 2
df['rolling_mean']  = df['Close'].rolling(window).mean()
rolling_std = df['Close'].rolling(window).std()
#create two new DataFrame columns to hold values of upper and lower Bollinger bands
df['BollingerHigh'] = df['rolling_mean'] + (rolling_std * no_of_std)
df['BollingerLow'] = df['rolling_mean'] - (rolling_std * no_of_std)

#Visualize the data
plt.figure(figsize=(16,8))
plt.title('Stock')
plt.xlabel('Date', fontsize=10)
plt.plot(df['ATR'], linewidth=1)
plt.plot(df['MFI'], linewidth=1)
plt.plot(df['Williamson'], linewidth=1)
plt.plot(df['ROC'], linewidth=1)
#plt.plot(df['CCI'], linewidth=1)
plt.legend(['ATR', 'MFI', 'Williamson', 'ROC', 'CCI'], loc='lower right')
#plt.plot(df['Close'], linewidth=1)
#plt.plot(df['BollingerHigh'], linewidth=1, color='green')
#plt.plot(df['BollingerLow'], linewidth=1, color='red')
#plt.legend(['Close', 'BollingerHigh', 'BollingerLow'], loc='lower right')
#plt.show()
plt.savefig('1.png')