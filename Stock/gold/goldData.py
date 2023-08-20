#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 01:10:44 2022

@author: pritamkhose

https://www.bankbazaar.com/gold-rate/gold-rate-trend-in-india.html

"""

import pandas as pd

# Importing the dataset
gdf = pd.read_csv('GoldRate.csv')

gdf = gdf.loc[gdf['Year'] > 1969]
gdf.reset_index(drop=True, inplace=True)

gdf['PriceOld']= gdf['Price'].shift(1)
gdf['PriceOld'][0] = gdf['Price'][0] 

gdf['PriceDiff'] = gdf.apply(lambda x: x['Price'] - x['PriceOld'], axis=1)
gdf['PricePercent'] = (gdf['PriceDiff'] / gdf['Price']) * 100

gdf['PricePercentMA'] = gdf['PricePercent'].rolling(window=5).mean()
gdf['PricePercentMA'].fillna(0,inplace=True)

# print(gdf["PricePercent"].mean())

gdf['ratio'] = gdf['Price'][0] 
gdf['ratio'] = gdf['Price'] / gdf['ratio']
