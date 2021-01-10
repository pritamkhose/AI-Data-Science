# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 21:53:38 2021

@author: Pritam

"""

# Import the libraries
import os
import glob

import math
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

import json
import requests

resultList = []
dp = 3

# Get Data
# compfiles = glob.glob("data/*.json")
compfiles = ['data\ICI02.json', 'data\IT.json', 'data\ITC.json']

for compname in compfiles:
    resultDict = {}
    cname = compname.replace('data\\', '').replace('.json', '')
    print(cname)
    # Read to json file
    with open(compname) as json_file:
        datajson = json.load(json_file)
    stock = datajson['g1']

    PVList = []
    for row in range(len(stock)):
        PVList.append([stock[row]['date'],
                       float(stock[row]['open']), float(stock[row]['close']),
                       float(stock[row]['low']), float(stock[row]['high']),
                       float(stock[row]['volume'])
                       ])
    df = pd.DataFrame(PVList, columns=[
                      'date', 'O', 'C', 'L', 'H', 'Vol'])
    
    dflen = len(df)
    
    df['P'] = (df['H'] + df['L'] + df['C'] )/3
    
    df['HL'] = df['H'] - df['L']
    df['OC'] = df['O'] - df['C'] 
    
    df['Y'] = df['C'].shift(1) - df['O'].shift(1)
    
    
    
    df['HLp'] = df['HL'] * 100 / df['P']
    df['OCp'] = df['OC'] * 100 / df['P']
    df['Yp'] = df['Y'] * 100 / df['P']
    
    df['Yoc'] = df['OCp'] > df['Yp']
    
    resultDict[cname] = [
     {'name': 'All', 'HLp' : round(df['HLp'].mean(), dp), 'OCp' :  round(df['OCp'].mean(), dp), 'Yp' :  round(df['Yp'].mean(), dp) },
     {'name': '1 W', 'HLp' : round(df['HLp'][dflen-5:dflen].mean(), dp), 'OCp' : round(df['OCp'][dflen-5:dflen].mean(), dp), 'Yp' : round(df['Yp'][dflen-5:dflen].mean(), dp) },
     {'name': '2 W', 'HLp' : round(df['HLp'][dflen-10:dflen].mean(), dp), 'OCp' : round(df['OCp'][dflen-10:dflen].mean(), dp), 'Yp' : round(df['Yp'][dflen-10:dflen].mean(), dp) },
     {'name': '1 M', 'HLp' : round(df['HLp'][dflen-20:dflen].mean(), dp), 'OCp' : round(df['OCp'][dflen-20:dflen].mean(), dp), 'Yp' : round(df['Yp'][dflen-20:dflen].mean(), dp) },
     {'name': '3 M', 'HLp' : round(df['HLp'][dflen-61:dflen].mean(), dp), 'OCp' : round(df['OCp'][dflen-61:dflen].mean(), dp), 'Yp' : round(df['Yp'][dflen-61:dflen].mean(), dp) },
     {'name': '6 M', 'HLp' : round(df['HLp'][dflen-124:dflen].mean(), dp), 'OCp' : round(df['OCp'][dflen-124:dflen].mean(), dp), 'Yp' : round(df['Yp'][dflen-124:dflen].mean(), dp) },
     {'name': '1 Y', 'HLp' : round(df['HLp'][dflen-250:dflen].mean(), dp), 'OCp' : round(df['OCp'][dflen-250:dflen].mean(), dp), 'Yp' : round(df['Yp'][dflen-250:dflen].mean(), dp) },
     {'name': '2 Y', 'HLp' : round(df['HLp'][dflen-500:dflen].mean(), dp), 'OCp' : round(df['OCp'][dflen-500:dflen].mean(), dp), 'Yp' : round(df['Yp'][dflen-500:dflen].mean(), dp) },
     {'name': '3 Y', 'HLp' : round(df['HLp'][dflen-750:dflen].mean(), dp), 'OCp' : round(df['OCp'][dflen-750:dflen].mean(), dp), 'Yp' : round(df['Yp'][dflen-750:dflen].mean(), dp) },
     ]
    
    resultList.append(resultDict)
    
    