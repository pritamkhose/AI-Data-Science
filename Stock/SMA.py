# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 19:02:04 2020

@author: Pritam
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
for row in range(len(df)):
    if(row < smaday):
        sma = 0
    else:
        sma = df['Close'][row-smaday:row].mean()
    PV = [df.index[row], sma]
    PVList.append(PV)    
df1 = pd.DataFrame(PVList, columns =['timedate', 'sma']) 


dffinal = df1.join(df, on='timedate', how='inner')

#Visualize the data
plt.figure(figsize=(16,8))
plt.title('Stock')
plt.xlabel('Date', fontsize=10)
plt.ylabel('Price USD ($)', fontsize=10)
plt.plot(dffinal['Close'], linewidth=1,)
plt.plot(dffinal['sma'], linewidth=1)
plt.legend(['Avg price', 'SMA',], loc='lower right')
#plt.show()
plt.savefig("1.png")