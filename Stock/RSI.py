# -*- coding: utf-8 -*-
"""
Created on Fri Apr 4 14:02:36 2020

@author: Pritam
https://en.wikipedia.org/wiki/Relative_strength_index
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

# RSI 14 Daily calculate
PVList=[]
for row in range(len(df)):
    diff = df['Close'][row]  - df['Close'][row -1]
    if(row == 0):
        U = 0
        D = 0
    elif(diff < 0):
        U = 0
        D = diff * -1
    else:
        U = diff
        D = 0
    PVList.append([row, diff, U, D])    
df2 = pd.DataFrame(PVList, columns =['index', 'diff', 'U', 'D']) 


PVList=[]
rsiday = 14;
for row in range(len(df2)):
    if(row < rsiday):
        smau = df2['U'][0:rsiday].mean()
        smad = df2['D'][0:rsiday].mean()
    else:
        smau = df2['U'][row-(rsiday-1):row+1].mean()
        smad = df2['D'][row-(rsiday-1):row+1].mean()
    RS = smau/smad
    RSI = 100 - (100/(1+RS))    
    PVList.append([RSI])
df3 = pd.DataFrame(PVList, columns =['RSI'])

dffinal = df2.join(df3, how='inner')


#Visualize the data
plt.figure(figsize=(16,8))
plt.title('Stock')
plt.xlabel('Date', fontsize=10)
plt.ylabel('Close Price', fontsize=10)
plt.plot(dffinal['index'], df['Close'], linewidth=1,)
plt.plot(dffinal['index'], dffinal['RSI'], linewidth=1,)
plt.plot(dffinal['index'], dffinal['U'], linewidth=1, color='green')
plt.plot(dffinal['index'], dffinal['D'], linewidth=1, color='red')
plt.legend(['Avg price', 'S3', 'R3', 'VWAP', 'SMA'], loc='lower right')
#plt.show()
plt.savefig("1.png")