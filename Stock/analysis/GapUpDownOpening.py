# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 14:16:04 2021

@author: Pritam
"""

from datetime import datetime
import os
import math
import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt


def getData(days):
    dirPath = 'E:\Code\python\AIDataScience\Stock\moneycontrol\data'
    data = []
    for path, subdirs, files in os.walk(dirPath):
        for name in files:
            if ".rar" in name:
                continue
            else:
                data.append(os.path.join(path, name))

    # data = [data[0], data[1], data[2]]

    stockList = []
    for fpath in data:
        try:
            fname = fpath.split('\\')
            fname = (fname[len(fname)-1]).replace('.json', '')
            # print(fname)

            df = pd.DataFrame(json.load(open(fpath))['g1'])
            df = df.drop(columns=['value'])
            df[['high', 'low', 'open', 'close', 'volume']] = df[[
                'high', 'low', 'open', 'close', 'volume']].astype(float)
            df['GapUP'] = df.open > df.high.shift()
            df['GapDown'] = df.open < df.low.shift()

            df['GapUPPer'] = (df.open - df.high.shift()) * df['GapUP']
            df['GapUPPer'] = df['GapUPPer'].replace({-0: np.nan})
            df['GapUPPer'] = (df['GapUPPer']*100) / df.open

            df['GapDownPer'] = (df.low.shift() - df.open) * df['GapDown']
            df['GapDownPer'] = df['GapDownPer'].replace({-0: np.nan})
            df['GapDownPer'] = (df['GapDownPer']*100) / df.open

            dflen = len(df)
            # take last 70 Week
            if(dflen-days) > 0:
                df = df[dflen-days:dflen]
            else:
                df

            countGapUP = (df.GapUP.value_counts()[1] * 100) / dflen
            countGapDown = (df.GapDown.value_counts()[1] * 100) / dflen
            stockList.append([fname, countGapUP, df['GapUPPer'].max(), df['GapUPPer'].mean(),  df['GapUPPer'].min(),
                              countGapDown, df['GapDownPer'].max(
            ), df['GapDownPer'].mean(),  df['GapDownPer'].min()
            ])  # , df
        except Exception as e:
            print(fname, str(e))

    resultdf = pd.DataFrame(stockList, columns=['name', 'GapUPper', 'GapUPmax', 'GapUPavg', 'GapUPmin',
                                                'GapDownper', 'GapDownmax', 'GapDownavg', 'GapDownmin'
                                                ])  # , 'df'
    return resultdf  # stockList


a = getData(250)
