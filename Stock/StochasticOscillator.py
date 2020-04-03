# -*- coding: utf-8 -*-
"""
Created on Fri Apr 4 14:02:36 2020

@author: Pritam
https://www.investopedia.com/terms/s/stochasticoscillator.asp
"""

#Import the libraries
import math
import pandas_datareader as web
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

#Get the stock quote
df = web.DataReader('INFY.NS', data_source='yahoo', start='2020-01-01', end='2020-04-03')

# Stochastic Oscillator Is 14 Daily calculate
PVList=[]
periodDay = 14;
for row in range(len(df)):
    C = df['Close'][row]
    if(row < periodDay):
        lowPeriod = df['Close'][0:periodDay].min()
        highPeriod = df['Close'][0:periodDay].max()
    else:
        lowPeriod = df['Close'][row-(periodDay-1):row+1].min()
        highPeriod = df['Close'][row-(periodDay-1):row+1].max()
    K = (C - lowPeriod)/(highPeriod - lowPeriod) * 100   
    PVList.append([row, K, lowPeriod, highPeriod]) 
df2 = pd.DataFrame(PVList, columns =['index', 'K', 'lowPeriod', 'highPeriod']) 

#Visualize the data
plt.figure(figsize=(16,8))
plt.title('Stock')
plt.xlabel('Date', fontsize=10)
plt.ylabel('Price USD ($)', fontsize=10)
plt.plot(df2['index'], df['Close'], linewidth=1,)
plt.plot(df2['index'], df2['K'],  linewidth=1, color='yellow')
plt.plot(df2['index'], df2['lowPeriod'], linewidth=1, color='green')
plt.plot(df2['index'], df2['highPeriod'], linewidth=1, color='red')
plt.legend(['Close price', 'K', 'lowPeriod', 'highPeriod'], loc='lower left')
#plt.show()
plt.savefig("1.png")