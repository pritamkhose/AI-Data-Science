# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 17:08:45 2021

@author: Pritam
"""

import os
import pandas as pd
import json


def getFiles():
    dirPath = 'E:\Code\python\AIDataScience\Stock\moneycontrol\data'
    data = []
    for path, subdirs, files in os.walk(dirPath):
        for name in files:
            if ".rar" in name:
                continue
            else:
                data.append(os.path.join(path, name))
    return data


def volumeYearRange(days):
    rangeList = [0, 0.25, 0.5, 0.75, 1, 1.5, 2, 2.5, 3, 4, 5, 6, 7, 8, 9, 10]
    stockList = []
    for fpath in getFiles():  # getFiles()[0:2]
        try:
            fname = fpath.split('\\')
            fname = (fname[len(fname)-1]).replace('.json', '')
            print(fname)

            df = pd.DataFrame(json.load(open(fpath))['g1'])
            df[['high', 'low', 'open', 'close', 'volume']] = df[[
                'high', 'low', 'open', 'close', 'volume']].astype(float)
            df = df[['date', 'close', 'volume']]

            df['volumeEMA20'] = df['volume'].ewm(span=20, adjust=False).mean()
            df['volumeEMA20'] = df['volume']/df['volumeEMA20']

            dflen = len(df)
            # # take last 300 days
            if(dflen-days) > 0:
                df = df[dflen-days:dflen]
            else:
                df

            aList = [fname]
            colList = ['mc_code']
            for row in range(len(rangeList)-1):
                name = 'vol_'+'L' + \
                    str(rangeList[row]) + 'H' + str(rangeList[row+1])
                colList.append(name)
                aList.append(
                    len(df[df['volumeEMA20'].between(rangeList[row], rangeList[row+1])]))
            stockList.append(aList)

        except Exception as e:
            print(fname, str(e))

    dfochl = pd.DataFrame(stockList, columns=colList)
    # dfochl.to_json('data/ochl_percent.json', orient='records', indent=2)
    return dfochl


dfochl = volumeYearRange(300)


def volumePriceRange(fpath, step, days):
    df = pd.DataFrame(json.load(open(fpath))['g1'])
    df[['close', 'volume']] = df[['close', 'volume']].astype(float)
    df = df[['date', 'close', 'volume']]

    df['volumeEMA20'] = df['volume'].ewm(span=20, adjust=False).mean()
    df['volumeEMA20'] = df['volume']/df['volumeEMA20']

    dflen = len(df)
    if(dflen-days) > 0:
        df = df[dflen-days:dflen]
    else:
        df
    dfmax = df.close.max()
    dfper = (dfmax/100)
    dfmax = dfmax/dfper
    dfmin = df.close.min()/dfper
    dfrange = (dfmax - dfmin) / step

    df['closePer'] = df.close/dfper

    rangeList = [dfmin]
    for i in range(step):
        rangeList.append(dfmin + (i+1) * dfrange)

    aList = []
    for row in range(len(rangeList)-1):
        aList.append([row, len(df[df['closePer'].between(rangeList[row], rangeList[row+1])]),
                      round((dfper * rangeList[row]), 2), round((dfper * rangeList[row+1]), 2)])
    return aList


fpath = 'E:\Code\python\AIDataScience\Stock\moneycontrol\data\IT.json'
alist = volumePriceRange(fpath, 20, 90)
