# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 19:02:04 2020

@author: Pritam
http://www.tradinggeeks.net/2014/05/technical-analysis-in-excel-part-i/
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

#Get the number of rows and columns in the data set
print(df.shape)

# SMA20 calculate
PVList=[]
smaday = 20;
period = 14;
stddev = 2;
for row in range(len(df)):
    if(row < smaday):
        sma20 = 0
    else:
        sma20 = df['Close'][row-smaday:row].mean()
    if(row < period):
        ema = df['Close'][row]
        smaGen = 0;
        bbuper = 0;
        bblower = 0;
    else:
        ema = df['Close'][row]*2/(1+period) +  PVList[row-1][2] * (1-2/(1+period))
        smaGen = ema #(OFFSET(H14,(-1*period+1),-4,period,1))/period
        bbuper = smaGen + stddev * (2) # H21+$P$3*STDEV(OFFSET(I21,(-1*$P$2+1),-5,$P$2,1))
        bblower = smaGen - stddev * (2) # H21-$P$3*STDEV(OFFSET(J21,(-1*$P$2+1),-6,$P$2,1))
    PV = [df.index[row], sma20, ema, smaGen, bbuper, bblower]
    PVList.append(PV)    
df1 = pd.DataFrame(PVList, columns =['timedate', 'sma20', 'ema', 'smaGen', 'bbuper', 'bblower']) 


dffinal = df1.join(df, on='timedate', how='inner')

#Visualize the data
plt.figure(figsize=(16,8))
plt.title('Stock')
plt.xlabel('Date', fontsize=10)
plt.ylabel('Price USD ($)', fontsize=10)
plt.plot(dffinal['Close'], linewidth=1)
plt.plot(dffinal['smaGen'], linewidth=1, color='yellow')
plt.plot(dffinal['bbuper'], linewidth=1, color='green')
plt.plot(dffinal['bblower'], linewidth=1, color='red')
plt.legend(['Avg price', 'BB Upper', 'BB Lower'], loc='lower right')
#plt.show()
plt.savefig("1.png")