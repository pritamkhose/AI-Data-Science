# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 11:27:22 2020

@author: Pritam

"""

#Import the libraries
import os
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#plt.style.use('fivethirtyeight')
import json
import requests

#1d 5d max
compname = 'IT'
#url = 'https://www.moneycontrol.com/mc/widget/basicchart/get_chart_value?classic=true&dur=max&sc_did=' + compname
#datajson = requests.get(url).json()
#
#if not os.path.exists('data'):
#    os.makedirs('data')
## Writing to json file
#with open('data/'+compname + '.json', 'w') as outfile: 
#    outfile.write(json.dumps(datajson))

# Read to json file
with open('data/'+compname + '.json') as json_file:
    datajson = json.load(json_file)

#newsdata = datajson['newsdata']
stock = datajson['g1']
PVList = [];
for row in range(len(stock)):
    PVList.append([pd.to_datetime(stock[row]['date']), stock[row]['date'], float(stock[row]['value']), 
                   float(stock[row]['open']) , float(stock[row]['close']), 
                   float(stock[row]['low']), float(stock[row]['high']), 
                   float(stock[row]['volume'])
                   ])
df = pd.DataFrame(PVList ,columns =['date', 'datestr','value', 'open', 'close', 'low', 'high', 'volume']) 


bdsList = [];
bonus = datajson['data']['bonus']
for row in range(len(bonus)):
    arr = (bonus[row]['ratio']).split(':')
    bdsList.append(['bonus', bonus[row]['date'].replace(', ','-'), arr[0], arr[1]])
    
dividends = datajson['data']['dividends']
for row in range(len(dividends)):
    arr = (dividends[row]['ratio']).split(' ')
    bdsList.append(['dividends', dividends[row]['date'].replace(', ','-'), arr[0], arr[1]])
    
splits = datajson['data']['splits']
for row in range(len(splits)):
    arr = (splits[row]['ratio']).split('-')
    bdsList.append(['splits',splits[row]['date'].replace(', ','-'), arr[0], arr[1]])
bdsdf = pd.DataFrame(bdsList ,columns =['type', 'date', 'para1', 'para2']) 
bdsdf = bdsdf.sort_values(by='date')
#bdsdf.index = bdsdf['date']

stockunit = 10
PVList = [];
bdsList = bdsdf.index.values.tolist()
for row in range(len(bdsList)):
    #if(bdsdf['date'][row] == stock[row]['date']) :
    print(bdsdf.iloc[[row]])
#    if(bdsdf['type'][row] == 'bonus') :
#        print(bdsdf.iloc[[row]])
#    elif(bdsdf['type'][row] == 'dividends') :
#        print(bdsdf.iloc[[row]])  
#    elif(bdsdf['type'][row] == 'splits') :
#        print(bdsdf.iloc[[row]])
#    else :
#        print(bdsdf.iloc[[row]])
        
#    netprice = stockunit * float(stock[row]['value'])
#    PVList.append([stockunit, netprice])
#df = pd.DataFrame(PVList ,columns =['date', 'value', 'open', 'close', 'low', 'high', 'volume', 'stockunit', 'netprice']) 




# df.index = df['date']


#vper =  1000000 #df['Volume'].mean()*0.1
##Visualize the data
#plt.figure(figsize=(16,8))
#plt.title('Stock ')
#plt.xlabel('Date', fontsize=10)
#plt.ylabel('Price', fontsize=10)
#plt.plot(df['value'], label = "Price", linewidth=1,)
#plt.plot((df['volume']/vper), label = "Volume", linewidth=1,)
#plt.legend()
#plt.grid()
#plt.savefig("1.png")
#plt.show()    