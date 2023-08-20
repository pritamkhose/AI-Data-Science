#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 21:10:44 2022

@author: pritamkhose

https://data.oecd.org/conversion/purchasing-power-parities-ppp.htm

"""

import pandas as pd

# Importing the dataset
df = pd.read_csv('DP_LIVE.csv')

df = df.loc[df['LOCATION'] == 'IND']

# print(df.columns)
# df = df.drop(['LOCATION', 'INDICATOR', 'SUBJECT', 'MEASURE', 'FREQUENCY', 'Flag Codes'], axis=1)
df.reset_index(drop=True, inplace=True)
df = df[['TIME', 'Value']]

df['ratio'] = df['Value'][0] 
df['ratio'] = df['Value'] / df['ratio']


df['ValueOld']= df['Value'].shift(1)
df['ValueOld'][0] = df['Value'][0] 
df['ValueDiff'] = df.apply(lambda x: x['Value'] - x['ValueOld'], axis=1)
df['ValuePercent'] = (df['ValueDiff'] / df['Value']) * 100
df['ValuePercentMA'] = df['ValuePercent'].rolling(window=5).mean()
df['ValuePercentMA'].fillna(0,inplace=True)