# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 11:27:22 2020

@author: Pritam

https://stackoverflow.com/questions/2817481/how-do-i-request-and-process-json-with-python
https://docs.atlas.mongodb.com/driver-connection/#driver-examples
python -m pip install numpy pandas matplotlib requests pymongo
"""


#Import the libraries
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#plt.style.use('fivethirtyeight')
import json

#Visualize the data
plt.figure(figsize=(16,8))
plt.title('Stock ')
plt.xlabel('Date', fontsize=10)
plt.ylabel('Price', fontsize=10)

#i = 'IT'
StockList = []
URLArr = ['ICI02','IT', 'RI', 'SBI', 'SC12','TCS', 'W', 'HSL01', 'HAM02'];
for i in URLArr:
    #Get the stock quote
    # Read json file in folder  
    with open('datajson/'+ i +'.json') as json_file:
        dataread = json.load(json_file)
    
    dflen = len(dataread['g1'])    
    df = pd.DataFrame(dataread['g1'][dflen-63:dflen])
    df['close'] = df['close'].astype('float64') 
    df['low'] = df['low'].astype('float64') 
    df['high'] = df['high'].astype('float64') 
    df['value'] = df['value'].astype('float64') 
    df['open'] = df['open'].astype('float64') 
    df['volume'] = df['volume'].astype('int64') 
    df['date'] = pd.to_datetime(df['date']) 
    
    PVList=[]
    shareQty = 10
    investprice = df['value'][0]  * shareQty
    investVol = df['volume'][0]
    
    for row in range(len(df)):
        price = df['value'][row] * shareQty
        percent = ((price - investprice)/investprice)*100
        chgper = ((df['high'][row] - df['low'][row])/ df['value'][row])*100
        volumeper =  (df['volume'][row]/investVol)*1
        PV = [price, percent, volumeper, chgper]
        PVList.append(PV)    
    df1 = pd.DataFrame(PVList, columns =['price', 'percent', 'volumeper', 'chgper']) 
    
    dffinal = df1.join(df, how='inner')
    StockList.append(dffinal)    
    
    x1 = list(range(0, len(df)))
    #x1 = df['date'].values.tolist()
    #import matplotlib.dates as mdates
    #myFmt = mdates.DateFormatter('%d')
    plt.plot(x1, dffinal['percent'].values.tolist(), label = i, linewidth=1)
#    #Visualize the data
#    plt.figure(figsize=(16,8))
#    plt.title('Stock '+ i)
#    plt.xlabel('Date', fontsize=10)
#    plt.ylabel('Price', fontsize=10)
#    plt.plot(x1, dffinal['chgper'].values.tolist(), label = "H/L chg per", linewidth=1, color='green')
#    plt.plot(x1, dffinal['volumeper'].values.tolist(), label = "volumeper", linewidth=1,color='orange')
#    plt.plot(x1, dffinal['percent'].values.tolist(), label = "loss profit", linewidth=1, color='blue')
#    plt.grid()
#    plt.legend( loc='lower left')
#    #plt.xaxis.set_major_formatter(myFmt)
#    plt.savefig('result/'i+'.png')
    #plt.show()    

plt.grid()
plt.legend( loc='lower left')
plt.savefig("result/result.png")   
plt.show()       