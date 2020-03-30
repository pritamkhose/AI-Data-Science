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

i = 'IT'
#for i in URLArr:
#Get the stock quote
# Read json file in folder    
with open('datajson/IT.json') as json_file:
    dataread = json.load(json_file)
    
shareQty = 10;

splits = dataread['data']['splits']
for row in range(len(splits)):
    sp = int(splits[row]['ratio'].split('-')[0])

print(shareQty * sp)
    
df = pd.DataFrame(dataread['g1'])
df['close'] = df['close'].astype('float64') 
df['low'] = df['low'].astype('float64') 
df['high'] = df['high'].astype('float64') 
df['value'] = df['value'].astype('float64') 
df['open'] = df['open'].astype('float64') 
df['volume'] = df['volume'].astype('int64') 
df['date'] = pd.to_datetime(df['date']) 

PVList=[]
investprice = df['value'][5000]  * shareQty
investVol = df['volume'][5000]

for row in range(len(df)):
    price = df['value'][row] * shareQty
    percent = ((price - investprice)/investprice)*100
    volumeper =  (df['volume'][row]/investVol)*100
    PV = [price, percent, volumeper]
    PVList.append(PV)    
df1 = pd.DataFrame(PVList, columns =['price', 'percent', 'volumeper']) 

dffinal = df1.join(df, how='inner')

start = 5000
end = len(dffinal)
y1 = dffinal['volumeper'].values.tolist()[start:end]
y2 = dffinal['percent'].values.tolist()[start:end] 
x1 = list(range(0, len(df)))[start:end]
#x1 = df['date'].values.tolist()


#Visualize the data
plt.figure(figsize=(16,8))
plt.title('Stock '+ i)
plt.xlabel('Date', fontsize=10)
plt.ylabel('Price', fontsize=10)
plt.plot(x1, y1, label = "value", linewidth=1,)
plt.plot(x1, y2, label = "percent", linewidth=1,)
plt.legend()
plt.grid()
plt.savefig("1.png")
plt.show()    