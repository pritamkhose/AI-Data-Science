# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 11:27:22 2020

@author: Pritam
https://charting.bseindia.com/index.html?SYMBOL=532174#

https://charting.bseindia.com/charting/RestDataProvider.svc/getDatI?exch=N&scode=500180&type=b&mode=bseL&fromdate=24-04-2020-04:00:03-PM
https://charting.bseindia.com/charting/RestDataProvider.svc/getDat?exch=N&scode=500180&type=b&mode=bseL&fromdate=01-01-1991-01:01:00-AM

"""


#Import the libraries
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#plt.style.use('fivethirtyeight')
import json
import requests
# icici 532174  infy 500209
url = 'https://charting.bseindia.com/charting/RestDataProvider.svc/getDat?exch=N&scode=500209&type=b&mode=bseL&fromdate=01-01-1991-01:01:00-AM'
datajson = json.loads(requests.post(url).json()['getDatResult'])
datainval = datajson['DataInputValues'][0]

OpenData = datainval['OpenData'][0]['Open'].split(",")
CloseData = datainval['CloseData'][0]['Close'].split(",")
LowValues = datainval['LowData'][0]['Low'].split(",")
VolumeData = datainval['VolumeData'][0]['Volume'].split(",")
DateData = datainval['DateData'][0]['Date'].split(",")

PVList = [];

for row in range(len(OpenData)):
    PVList.append([row, pd.to_datetime(DateData[row]), float(OpenData[row]) , float(CloseData[row]), float(LowValues[row]), float(VolumeData[row])])
df = pd.DataFrame(PVList, columns =['Index','Date', 'Open', 'Close', 'Low', 'Volume']) 

vper =  10000 #df['Volume'].mean()*0.1
#Visualize the data
plt.figure(figsize=(16,8))
plt.title('Stock ')
plt.xlabel('Date', fontsize=10)
plt.ylabel('Price', fontsize=10)
plt.plot(df['Index'], df['Open'], label = "Price", linewidth=1,)
plt.plot((df['Volume']/vper), label = "Volume", linewidth=1,)
plt.legend()
plt.grid()
plt.savefig("1.png")
plt.show()    