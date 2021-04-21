# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 18:17:18 2021

@author: Pritam
"""

import os
import pandas as pd


if not os.path.exists('data/'):
    os.makedirs('data/')

with pd.HDFStore('./FullData.h5') as hdf:
    # This prints a list of all group names:
    FullDataKeys = hdf.keys()

# df = pd.read_hdf('./FullData.h5', key='/INFY__EQ__NSE__NSE__MINUTE')
# df.to_json('infy.json')

keys = [
'/NIFTY_50__EQ__INDICES__NSE__MINUTE',
'/NIFTY_BANK__EQ__INDICES__NSE__MINUTE',
'/TCS__EQ__NSE__NSE__MINUTE',
'/WIPRO__EQ__NSE__NSE__MINUTE',
'/INFY__EQ__NSE__NSE__MINUTE'
]

for key in keys:
    df = pd.read_hdf('./FullData.h5', key=key)
    fname = key.replace('__EQ__INDICES__NSE__MINUTE', '')
    fname = fname.replace('__EQ__NSE__NSE__MINUTE', '')
    # df.to_json('data'+ fname +'.json')
    df.to_csv('data'+ fname +'.csv')