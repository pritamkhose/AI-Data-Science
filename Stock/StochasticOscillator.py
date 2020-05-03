# -*- coding: utf-8 -*-
"""
Created on Fri Apr 4 14:02:36 2020

@author: Pritam
https://www.investopedia.com/terms/s/stochasticoscillator.asp

https://www.pythonforfinance.net/2017/10/10/stochastic-oscillator-trading-strategy-backtest-in-python/
"""

#Import the libraries
import math
import pandas_datareader as web
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

#Get the stock quote
df = web.DataReader('INFY.NS', data_source='yahoo', start='2010-01-01', end='2020-05-02')

# Stochastic Oscillator Is 14 Daily calculate
#PVList=[]
#periodDay = 14;
#for row in range(len(df)):
#    C = df['Close'][row]
#    if(row < periodDay):
#        lowPeriod = df['Close'][0:periodDay].min()
#        highPeriod = df['Close'][0:periodDay].max()
#    else:
#        lowPeriod = df['Close'][row-(periodDay-1):row+1].min()
#        highPeriod = df['Close'][row-(periodDay-1):row+1].max()
#    K = (C - lowPeriod)/(highPeriod - lowPeriod) * 100   
#    PVList.append([row, K, lowPeriod, highPeriod]) 
#df2 = pd.DataFrame(PVList, columns =['index', 'K', 'lowPeriod', 'highPeriod']) 

##Visualize the data
#plt.figure(figsize=(16,8))
#plt.title('Stock')
#plt.xlabel('Date', fontsize=10)
#plt.ylabel('Price USD ($)', fontsize=10)
#plt.plot(df2['index'], df['Close'], linewidth=1,)
#plt.plot(df2['index'], df2['K'],  linewidth=1, color='yellow')
#plt.plot(df2['index'], df2['lowPeriod'], linewidth=1, color='green')
#plt.plot(df2['index'], df2['highPeriod'], linewidth=1, color='red')
#plt.legend(['Close price', 'K', 'lowPeriod', 'highPeriod'], loc='lower left')
##plt.show()
#plt.savefig("1.png")


##Create the "L14" column in the DataFrame
#df['L14'] = df['Low'].rolling(window=14).min()
##Create the "H14" column in the DataFrame
#df['H14'] = df['High'].rolling(window=14).max()
##Create the "%K" column in the DataFrame
#df['%K'] = 100*((df['Close'] - df['L14']) / (df['H14'] - df['L14']) )
##Create the "%D" column in the DataFrame
#df['%D'] = df['%K'].rolling(window=3).mean()
#
#fig, axes = plt.subplots(nrows=2, ncols=1,figsize=(20,10))
#df['Close'].plot(ax=axes[0], linewidth=1,); axes[0].set_title('Close')
#df[['%K','%D']].plot(ax=axes[1], linewidth=1,); axes[1].set_title('Oscillator')
#
##Create a column in the DataFrame showing "TRUE" if sell entry signal is given and "FALSE" otherwise. 
##A sell is initiated when the %K line crosses down through the %D line and the value of the oscillator is above 80 
#df['Sell Entry'] = ((df['%K'] < df['%D']) & (df['%K'].shift(1) > df['%D'].shift(1))) & (df['%D'] > 80) 
##Create a column in the DataFrame showing "TRUE" if sell exit signal is given and "FALSE" otherwise. 
##A sell exit signal is given when the %K line crosses back up through the %D line 
#df['Sell Exit'] = ((df['%K'] > df['%D']) & (df['%K'].shift(1) < df['%D'].shift(1))) 
##create a placeholder column to populate with short positions (-1 for short and 0 for flat) using boolean values created above 
#df['Short'] = np.nan 
#df.loc[df['Sell Entry'],'Short'] = -1 
#df.loc[df['Sell Exit'],'Short'] = 0 
##Set initial position on day 1 to flat 
#df['Short'][0] = 0 
##Forward fill the position column to represent the holding of positions through time 
#df['Short'] = df['Short'].fillna(method='pad') 
##Create a column in the DataFrame showing "TRUE" if buy entry signal is given and "FALSE" otherwise. 
##A buy is initiated when the %K line crosses up through the %D line and the value of the oscillator is below 20 
#df['Buy Entry'] = ((df['%K'] > df['%D']) & (df['%K'].shift(1) < df['%D'].shift(1))) & (df['%D'] < 20) 
##Create a column in the DataFrame showing "TRUE" if buy exit signal is given and "FALSE" otherwise. 
##A buy exit signal is given when the %K line crosses back down through the %D line 
#df['Buy Exit'] = ((df['%K'] < df['%D']) & (df['%K'].shift(1) > df['%D'].shift(1))) 
##create a placeholder column to polulate with long positions (1 for long and 0 for flat) using boolean values created above 
#df['Long'] = np.nan  
#df.loc[df['Buy Entry'],'Long'] = 1  
#df.loc[df['Buy Exit'],'Long'] = 0  
##Set initial position on day 1 to flat 
#df['Long'][0] = 0  
##Forward fill the position column to represent the holding of positions through time 
#df['Long'] = df['Long'].fillna(method='pad') 
##Add Long and Short positions together to get final strategy position (1 for long, -1 for short and 0 for flat) 
#df['Position'] = df['Long'] + df['Short']
#
#
#df['Position'].plot(figsize=(20,10))
#
#
##Set up a column holding the daily Apple returns
#df['Market Returns'] = df['Close'].pct_change()
##Create column for Strategy Returns by multiplying the daily Apple returns by the position that was held at close
##of business the previous day
#df['Strategy Returns'] = df['Market Returns'] * df['Position'].shift(1)
##Finally plot the strategy returns versus Apple returns
#df[['Strategy Returns','Market Returns']].cumsum().plot()



df['L14'] = df['Low'].rolling(window=14).min()
df['H14'] = df['High'].rolling(window=14).max()
df['%K'] = 100*((df['Close'] - df['L14']) / (df['H14'] - df['L14']) )
df['%D'] = df['%K'].rolling(window=3).mean()
df['Sell Entry'] = ((df['%K'] < df['%D']) & (df['%K'].shift(1) > df['%D'].shift(1))) & (df['%D'] > 80)
df['Buy Entry'] = ((df['%K'] > df['%D']) & (df['%K'].shift(1) < df['%D'].shift(1))) & (df['%D'] < 20)
#Create empty "Position" column
df['Position'] = np.nan 
#Set position to -1 for sell signals
df.loc[df['Sell Entry'],'Position'] = -1 
#Set position to -1 for buy signals
df.loc[df['Buy Entry'],'Position'] = 1 
#Set starting position to flat (i.e. 0)
df['Position'].iloc[0] = 0 
#Forward fill the position column to show holding of positions through time
df['Position'] = df['Position'].fillna(method='ffill')
#Set up a column holding the daily Apple returns
df['Market Returns'] = df['Close'].pct_change()
#Create column for Strategy Returns by multiplying the daily Apple returns by the position that was held at close
#of business the previous day
df['Strategy Returns'] = df['Market Returns'] * df['Position'].shift(1)
#Finally plot the strategy returns versus Apple returns
df[['Strategy Returns','Market Returns']].cumsum().plot(figsize=(20,10))