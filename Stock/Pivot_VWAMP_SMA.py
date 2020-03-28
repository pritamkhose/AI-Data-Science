# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 10:57:18 2020

@author: Pritam
https://www.investopedia.com/ask/answers/122414/what-moving-average-convergence-divergence-macd-formula-and-how-it-calculated.asp

"""

#Import the libraries
import math
import pandas_datareader as web
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

#Get the stock quote
#df = web.DataReader('AAPL', data_source='yahoo', start='2012-01-01', end='2019-12-17')
df = web.DataReader('INFY', data_source='yahoo', start='2018-01-01', end='2020-03-27')
#Show teh data
#print(df)

#Get the number of rows and columns in the data set
print(df.shape)

def moving_average(arr, n):
    return [ (arr[:i+1][::-1][:n]).mean() for i, ele in enumerate(arr) ]

# Pivot VWAMP calculate
PVList = []
sumVol = 0;
for row in range(len(df)):
    H = df['High'][row]
    L = df['Low'][row]
    C = df['Close'][row]
    vol =  df['Volume'][row]
    P = (H + L + C)/3
    R1 = P + (P - L) # R1 = 2*P - L
    S1 = P - (H - P) # S1 = 2*P - H
    R2 = P + (H - L)
    S2 = P - (H - L)
    R3 = R1 + (H - L) # R3 = H + 2*(P - L) 
    S3 = S1 - (H - L) # S3 = L - 2*(H - P) 
    VP = P * vol
    sumVol = sumVol + vol
    VWAMP = VP / sumVol
    PV = [df.index[row], P, R1, S1, R2, S2, R3, S3 , VP, sumVol, VWAMP]
    PVList.append(PV)
df2 = pd.DataFrame(PVList, columns =['timedate', 'P', 'R1', 'S1', 'R2', 'S2', 'R3', 'S3', 'VP', 'sumVol', 'VWAMP']) 

PVList=[]
smaday = 20;
for row in range(len(df2)):
    if(row < smaday):
        sma = 0
    else:
        sma = df2['P'][row-smaday:row].mean()
    PV = [sma]
    PVList.append(PV)    
df3 = pd.DataFrame(PVList, columns =['sma']) 
dffinal = df2.join(df3, how='inner')

#Visualize the data
plt.figure(figsize=(16,8))
plt.title('Stock')
plt.xlabel('Date', fontsize=10)
plt.ylabel('Price USD ($)', fontsize=10)
plt.plot(df2['S3'], linewidth=1,)
plt.plot(df2['R3'], linewidth=1,)
plt.plot(dffinal['sma'], linewidth=1,)
plt.legend(['Avg price', 'P', 'S3', 'R3'], loc='lower right')
#plt.show()
plt.savefig("1.png")