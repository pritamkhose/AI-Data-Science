# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 11:23:32 2021

@author: Pritam
"""

#Import the libraries
import os
import math
import numpy as np
import pandas as pd
import json
import requests


compname = 'IT' #'W' or 'IT' as 14 is Result date  

# url = 'https://www.moneycontrol.com/mc/widget/basicchart/get_chart_value?classic=true&dur=max&sc_did=' + compname
# # url = 'https://www.moneycontrol.com/mc/widget/basicchart/get_chart_value?classic=true&dur=5d&sc_did=' + compname
# datajson = requests.get(url).json()
# df = pd.DataFrame(datajson['g1'])

# df = df.drop(['value'], axis = 1) 
# df[['high', 'low','open', 'close', 'volume']] = df[['high', 'low','open', 'close', 'volume']].astype(float)
# df.to_json(compname + '.json', orient='records')

# Read json file in folder  
with open(compname + '.json') as json_file:
    dataread = json.load(json_file)   
df = pd.DataFrame(dataread)


s = ''
for x in range(11,21):
    x = str(x)
    if(len(x) == 1):
        s = s + '200'+ x + '-|'
    else :
        s = s + '20'+ x + '-|'
df['sel'] = df['date'].str.contains(s[:-1])
df = df.drop(df[df['sel'] == False].index)
df = df.reset_index()


df['P'] = (df['high'] + df['low']+ df['close'])/3
df['Ppev'] = df['P'] - df['P'].shift(1)
df['P10'] = df['P'].rolling(window=14).mean()

df['cpev'] = df['close'] - df['close'].shift(1)
df['c10'] = df['close'].rolling(window=14).mean()

df['vpev'] = df['volume'] - df['volume'].shift(1)
df['vol10'] = df['volume'].rolling(window=14).mean()

# df['opev'] = df['open'] - df['open'].shift(1)
# df['hpev'] = df['high'] - df['high'].shift(1)
# df['lpev'] = df['low'] - df['low'].shift(1)

df['c10per'] =( df['close'] * 100)/ df['c10']
df['P10per'] =( df['P'] * 100)/ df['P10']
df['vol10per'] =( df['volume'] * 100)/ df['vol10']

# df = df.drop(df[df['vol10per'] <= 100].index)

## Sell
df = df.drop(df[df['c10per'] <= 100].index)
df = df.drop(df[df['P10per'] <= 100].index)
df.sort_values(by=['P10per', 'c10per'], ascending=False)

## Buy
# df = df.drop(df[df['c10per'] >= 100].index)
# df = df.drop(df[df['P10per'] >= 100].index)