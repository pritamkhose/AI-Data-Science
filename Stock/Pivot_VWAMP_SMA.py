# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 10:57:18 2020

@author: Pritam
https://www.investopedia.com/ask/answers/122414/what-moving-average-convergence-divergence-macd-formula-and-how-it-calculated.asp
https://stockstotrade.com/pivot-points/
https://www.mypivots.com/dictionary/definition/42/camarilla-pivot-points
https://www.investopedia.com/terms/m/movingaverage.asp
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
df = web.DataReader('INFY.NS', data_source='yahoo', start='2020-01-01', end='2020-04-03')
#Show teh data
#print(df)

#Get the number of rows and columns in the data set
print(df.shape)

def moving_average(arr, n):
    return [ (arr[:i+1][::-1][:n]).mean() for i, ele in enumerate(arr) ]

# Pivot Daily calculate
PVList = []
sumVol = 0;
for row in range(len(df)):
    H = df['High'][row]
    L = df['Low'][row]
    C = df['Close'][row]
    vol =  df['Volume'][row]
    P = (H + L + C)/3
    
#    #Classic
    R1 = P + (P - L) # R1 = 2*P - L
    S1 = P - (H - P) # S1 = 2*P - H
    R2 = P + (H - L)
    S2 = P - (H - L)
    R3 = R1 + (H - L) # R3 = H + 2*(P - L) 
    S3 = S1 - (H - L) # S3 = L - 2*(H - P)
    
#    #Fibonacci
#    R1 = P + (0.382 * (H - L))
#    S1 = P - (0.382 * (H - L))
#    R2 = P + (0.618 * (H - L))
#    S2 = P - (0.618 * (H - L))
#    R3 = P + (1 * (H - L)) 
#    S3 = P - (1 * (H - L))
    
#    #Camarilla
#    RANGE = H - L
#    R4 = C + RANGE * 1.1/2
#    R3 = C + RANGE * 1.1/4
#    R2 = C + RANGE * 1.1/6
#    R1 = C + RANGE * 1.1/12
#    S1 = C - RANGE * 1.1/12
#    S2 = C - RANGE * 1.1/6
#    S3 = C - RANGE * 1.1/4
#    S4 = C - RANGE * 1.1/2
    
    VP = C * vol
    PV = [df.index[row], P, R1, S1, R2, S2, R3, S3 , VP]
    PVList.append(PV)
df2 = pd.DataFrame(PVList, columns =['timedate', 'P', 'R1', 'S1', 'R2', 'S2', 'R3', 'S3', 'VP']) 
PVList=[]
smaday = 14; #10, 20, 50, 100, 200
for row in range(len(df2)):
    if(row < smaday):
        sma = df['Close'][0:smaday].mean()
        sumVol = df['Volume'][0:smaday+1].sum()
        sumVolP = df2['VP'][0:smaday+1].sum()
    else:
        sma = df['Close'][row-(smaday-1):row+1].mean()
        sumVol = df['Volume'][row-(smaday-1):row+1].sum()
        sumVolP = df2['VP'][row-(smaday-1):row+1].sum()
    VWAP = sumVolP / sumVol
    PV = [sma, VWAP]
    PVList.append(PV)    
df3 = pd.DataFrame(PVList, columns =['sma','VWAP']) 
dffinal = df2.join(df3, how='inner')

#Visualize the data
plt.figure(figsize=(16,8))
plt.title('Stock')
plt.xlabel('Date', fontsize=10)
plt.ylabel('Price USD ($)', fontsize=10)
plt.plot(dffinal['P'], linewidth=1,)
plt.plot(df2['S3'], linewidth=1,)
plt.plot(df2['R3'], linewidth=1,)
plt.plot(dffinal['VWAP'], linewidth=1,)
plt.plot(dffinal['sma'], linewidth=1,)
plt.legend(['Avg price', 'S3', 'R3', 'VWAP', 'SMA'], loc='lower right')
#plt.show()
plt.savefig("1.png")