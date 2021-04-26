# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 15:52:06 2021

@author: Pritam
"""
from datetime import datetime
import os
import math
import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt


def getData():
    dirPath = 'E:\Code\python\AIDataScience\Stock\moneycontrol\data'
    data = []
    for path, subdirs, files in os.walk(dirPath):
        for name in files:
            if ".rar" in name:
                continue
            else:
                data.append(os.path.join(path, name))

    # data = [data[0], data[2]]

    stockList = []
    for fpath in data:
        try:
            fname = fpath.split('\\')
            fname = (fname[len(fname)-1]).replace('.json', '')
            print(fname)

            df = pd.DataFrame(json.load(open(fpath))['g1'])
            df[['high', 'low', 'open', 'close', 'volume']] = df[[
                'high', 'low', 'open', 'close', 'volume']].astype(float)

            # # take last 1Y or 250 days but week time frame
            df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
            df.set_index('date', inplace=True)
            df = calcHLOCV(df, 'W')

            dflen = len(df)
            # # take last 1Y or 250 days
            # df = df[dflen-250:dflen]

            # take last 70 Week
            if(dflen-70) > 0:
                df = df[dflen-70:dflen]
            else:
                df

            df['hl'] = df.high - df.low
            df['oc'] = df.open - df.close
            df['oc'] = df['oc'].abs()

            df['hlp'] = (df['hl'] * 100)/df.close
            df['ocp'] = (df['oc'] * 100)/df.close

            # rangeList = [0,0.25,0.5,0.75,1,1.5,2,2.5,3,4,5,6,7,8,9,10,15,20,100]
            rangeList = [0, 0.5, 1, 1.5, 2, 2.5, 3,
                         4, 5, 6, 7, 8, 9, 10, 15, 20, 100]
            aList = [fname]
            colList = ['mc_code']
            for row in range(len(rangeList)-1):
                name = 'ocp_'+'L' + \
                    str(rangeList[row]) + 'H' + str(rangeList[row+1])
                colList.append(name)
                aList.append(
                    len(df[df['ocp'].between(rangeList[row], rangeList[row+1])]))
            for row in range(len(rangeList)-1):
                name = 'hlp_'+'L' + \
                    str(rangeList[row]) + 'H' + str(rangeList[row+1])
                colList.append(name)
                aList.append(
                    len(df[df['ocp'].between(rangeList[row], rangeList[row+1])]))
            stockList.append(aList)
        except Exception as e:
            print(fname, str(e))

    dfochl = pd.DataFrame(stockList, columns=colList)
    dfochl.to_json('data/ochl_percent.json', orient='records', indent=2)


def calcHLOCV(df, sample):
    dfH = df.high.resample(sample).max().to_frame()
    dfL = df.low.resample(sample).min().to_frame()
    dfO = df.open.resample(sample).first().to_frame()
    dfC = df.close.resample(sample).last().to_frame()
    dfV = df.volume.resample(sample).sum().to_frame()
    PVList = []
    for row in range(len(dfH)):
        PV = [dfH.index[row], dfH['high'][row], dfL['low'][row],
              dfO['open'][row], dfC['close'][row], dfV['volume'][row]]
        PVList.append(PV)
    return pd.DataFrame(PVList, columns=['time', 'high', 'low', 'open', 'close', 'volume'])


def analyzeData():
    dfochl = pd.DataFrame(json.load(open('data/ochl_percent.json')))
    dfcomp = pd.DataFrame(
        json.load(open('E:\Code\python\Stock\StockAPI\extra\stock_bse_nse_mc.json')))
    dfcomp = dfcomp[['mc_code', 'comp_name']]
    result = pd.merge(dfcomp, dfochl, how='inner', on='mc_code')

    ocpList = []
    for item in result.columns:
        if item.find("ocp_") != -1:
            ocpList.append(item)
    resultOCP = result[ocpList]
    resultOCP["sum"] = resultOCP.sum(axis=1)
    resultOCP["sum"] = resultOCP["sum"] / 100
    for item in resultOCP.columns:
        resultOCP[item] = resultOCP[item] / resultOCP["sum"]
    resultOCP = dfcomp.join(resultOCP)

    hlpList = []
    for item in result.columns:
        if item.find("hlp_") != -1:
            hlpList.append(item)
    resultHLP = result[hlpList]
    resultHLP["sum"] = resultHLP.sum(axis=1)
    resultHLP["sum"] = resultHLP["sum"] / 100
    for item in resultHLP.columns:
        resultHLP[item] = resultHLP[item] / resultHLP["sum"]
    resultHLP = dfcomp.join(resultHLP)
    return {'open_close_percent': resultOCP, 'high_low_percent': resultHLP}


getData()
result = analyzeData()
