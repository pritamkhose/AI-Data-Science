#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 11:59:45 2023

@author: pritamkhose
"""

# Import lib
from datetime import datetime
import time
import os
from pathlib import Path
import glob
import json
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

url = 'https://charting.bseindia.com/charting/RestDataProvider.svc/getDat?exch=N&type=b&mode=bseL&fromdate=01-01-2021-01:01:00-AM&scode='
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}
id = '500470' # '500325'
folderPath = ''
filePath = os.path.join(folderPath, id + '.json')

forceUpdate = False

durFlag = 'i'  # 'i'
if(durFlag):
    folderPath = ''
    url = url.replace('getDat?', 'getDatI?')
if(durFlag):
    data = requests.post( url + id, headers=headers).json()['getDatIResult']
else:
    data = requests.post(url + id, headers=headers).json()['getDatResult']

data = (json.loads(data))['DataInputValues'][0]
OpenData = data['OpenData'][0]['Open'].split(",")
CloseData = data['CloseData'][0]['Close'].split(",")
LowValues = data['LowData'][0]['Low'].split(",")
HighData = data['HighData'][0]['High'].split(",")
VolumeData = data['VolumeData'][0]['Volume'].split(",")
DateData = data['DateData'][0]['Date'].split(",")
PVList = []
for row in range(len(OpenData)-1):
    PVList.append([DateData[row], OpenData[row],
                   CloseData[row], HighData[row], LowValues[row], VolumeData[row]])
df = pd.DataFrame(
    PVList, columns=['time', 'open', 'close', 'high', 'low', 'volume'])
df[['high', 'low', 'open', 'close', 'volume']] = df[[
    'high', 'low', 'open', 'close', 'volume']].astype(float)
if(durFlag):
      # df['time'] = (pd.to_datetime(df['time'], format='%d/%m/%Y %H:%M:%S %p')
                        #               ).dt.strftime('%Y-%m-%d-%H-%M').astype('str')
    df['time'] = (pd.to_datetime(df['time'], format='%d/%m/%Y %H:%M:%S %p'))
else:
    df['time'] = (pd.to_datetime(df['time'], format='%d/%m/%Y %H:%M:%S %p')).dt.strftime('%Y-%m-%d').astype('str')

df.to_json(folderPath + id + '.json', orient='records')
with open(filePath) as f:
    fdata = json.load(f)
dataObj = {'chart': fdata}
