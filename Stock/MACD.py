# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 11:47:49 2020

@author: Pritam
http://investexcel.net/how-to-calculate-macd-in-excel/
"""

#Import the libraries
import math
import pandas_datareader as web
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

#Get the stock quote
df = web.DataReader('INFY', data_source='yahoo', start='2018-01-01', end='2020-03-27')

PVList=[]
emaday12 = 12;
emaday26 = 26;
emaday9 = 9;
for row in range(len(df)):
    # calculate ema 12
    if(row < emaday12):
        ema12 = 0
    elif(row == emaday12):
        ema12 = df['Close'][row-emaday12:row].mean()
    else:
        ema12 = (df['Close'][row]*(2/(emaday12+1))) + (PVList[row-1][1]*(1-(2/(emaday12+1))))
    # calculate ema 26
    if(row < emaday26):
        ema26 = 0
    elif(row == emaday26):
        ema26 = df['Close'][row-emaday26:row].mean()
    else:
        ema26 = (df['Close'][row]*(2/(emaday26+1))) + (PVList[row-1][2]*(1-(2/(emaday26+1))))
    
    macd = 0
    signal = 0
    if(row >= emaday26):
        macd = ema12-ema26
        signal = (macd*(2/(emaday9+1))+PVList[row-1][4]*(1-(2/(emaday9+1))))
    histogram = macd - signal
    PV = [df.index[row], ema12, ema26, macd, signal, histogram]
    PVList.append(PV)   
    
 
df3 = pd.DataFrame(PVList, columns =['timedate', 'ema12', 'ema26', 'macd', 'signal', 'histogram']) 
dffinal = df3.join(df, on='timedate', how='inner')

#Visualize the data
plt.figure(figsize=(16,8))
plt.title('Stock')
plt.xlabel('Date', fontsize=10)
plt.ylabel('Price USD ($)', fontsize=10)
plt.plot(dffinal['Close'], linewidth=1)
plt.plot(dffinal['macd'], linewidth=1, color='green')
plt.plot(dffinal['signal'], linewidth=1, color='red')
plt.plot(dffinal['histogram'], linewidth=1, color='yellow')
plt.legend(['Avg price', 'P', 'sma12'], loc='lower right')
#plt.show()
plt.savefig("1.png")