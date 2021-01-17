# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 21:21:41 2021

@author: Pritam

"""
#Import the libraries
import os
import math
import numpy as np
import pandas as pd
import json
import requests


compname = 'W' #'W' or 'IT' as 14 is Result date  

url = 'https://www.moneycontrol.com/mc/widget/basicchart/get_chart_value?classic=true&dur=max&sc_did=' + compname
# url = 'https://www.moneycontrol.com/mc/widget/basicchart/get_chart_value?classic=true&dur=5d&sc_did=' + compname
datajson = requests.get(url).json()
df = pd.DataFrame(datajson['g1'])

df = df.drop(['value'], axis = 1) 
df[['high', 'low','open', 'close', 'volume']] = df[['high', 'low','open', 'close', 'volume']].astype(float)
df.to_json(compname + '.json', orient='records')

# Read json file in folder  
with open(compname + '.json') as json_file:
    dataread = json.load(json_file)   
df = pd.DataFrame(dataread)

df['datestr'] = df['date']
df['P'] = (df['high'] + df['low']+ df['close'])/3
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
df.set_index('date', inplace = True) 

def calcHLOCV(df, sample):
    dfH = df.high.resample(sample).max().to_frame() 
    dfL = df.low.resample(sample).min().to_frame() 
    dfO = df.open.resample(sample).first().to_frame() 
    dfC = df.close.resample(sample).last().to_frame() 
    dfP = df.P.resample(sample).mean().to_frame() 
    dfV = df.volume.resample(sample).sum().to_frame() 
    
    PVList=[]
    for row in range(len(dfH)):
        PV = [dfH.index[row], dfH['high'][row], dfL['low'][row], dfO['open'][row], dfC['close'][row], dfP['P'][row], dfV['volume'][row]]
        PVList.append(PV)    
    return pd.DataFrame(PVList, columns =['date', 'high', 'low', 'open', 'close', 'P', 'volume'])


s = ''
for x in range(1,20):
    x = str(x)
    if(len(x) == 1):
        s = s + '-01-0'+ x + '|'
    else :
        s = s + '-01-'+ x + '|'
    if(len(x) == 1):
        s = s + '-04-0'+ x + '|'
    else :
        s = s + '-04-'+ x + '|'
    if(len(x) == 1):
        s = s + '-07-0'+ x + '|'
    else :
        s = s + '-07-'+ x + '|'
    if(len(x) == 1):
        s = s + '-10-0'+ x + '|'
    else :
        s = s + '-10-'+ x + '|'
for x in range(24, 31):
    x = str(x)
    if(len(x) == 1):
        s = s + '-12-0'+ x + '|'
    else :
        s = s + '-12-'+ x + '|'
    if(len(x) == 1):
        s = s + '-03-0'+ x + '|'
    else :
        s = s + '-03-'+ x + '|'
    if(len(x) == 1):
        s = s + '-06-0'+ x + '|'
    else :
        s = s + '-06-'+ x + '|'
    if(len(x) == 1):
        s = s + '-09-0'+ x + '|'
    else :
        s = s + '-09-'+ x + '|'
df['sel'] = df['datestr'].str.contains(s[:-1])


df = df.drop(df[df['sel'] == False].index)
df['month'] = df.index.values.astype('datetime64[M]')

dmon = df['month'].unique() #.astype('str')

PVList=[]
for x in dmon:
    dftemp = df[df['month'] == x]
    dftemp = dftemp.reset_index()
    dftemplen = len(dftemp) -1
    close = dftemp['close'][dftemplen] - dftemp['close'][0]
    low = dftemp['low'][dftemplen] - dftemp['low'][0]
    high = dftemp['high'][dftemplen] - dftemp['high'][0]
    openp = dftemp['open'][dftemplen] - dftemp['open'][0]
    p = dftemp['P'][dftemplen] - dftemp['P'][0]
    hl = dftemp['high'].max() - dftemp['low'].min()
    
    pper = (p * 100) / dftemp['P'][0]
    cper = (close * 100) / dftemp['close'][0]
    hlper = (hl * 100) / dftemp['low'].min()
    hlperp = (hl * 100) / dftemp['P'].mean()
    
    PVList.append([dftemp['month'][0], dftemplen+1, close, p, openp, high, low, hl, pper, cper, hlper, hlperp])
resultDF = pd.DataFrame(PVList, columns =['date', 'workday', 'close', 'P', 'open', 'high', 'low', 'hl', 'pper', 'cper', 'hlper', 'hlperp'])

print(resultDF['cper'].mean(), resultDF['cper'].min(), resultDF['cper'].max())