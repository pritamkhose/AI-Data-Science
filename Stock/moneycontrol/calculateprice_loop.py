# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 11:27:22 2020

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
# Get Data
compfiles = glob.glob("data/*.json")
# compfiles = ['data\AB16.json', 'data\AC18.json', 'data\ADANI54145.json']
compfiles = ['data\AI51.json']

for compname in compfiles:
    cname = compname.replace('data\\', '').replace('.json', '')
    print(cname)
    # Read to json file
    with open(compname) as json_file:
        datajson = json.load(json_file)
    stock = datajson['g1']

    PVList = []
    for row in range(len(stock)):
        PVList.append([pd.to_datetime(stock[row]['date']), stock[row]['date'], float(stock[row]['value']),
                       float(stock[row]['open']), float(stock[row]['close']),
                       float(stock[row]['low']), float(stock[row]['high']),
                       float(stock[row]['volume'])
                       ])
    df = pd.DataFrame(PVList, columns=[
                      'date', 'datestr', 'value', 'open', 'close', 'low', 'high', 'volume'])

    bdsList = []

    try:
        bonus = datajson['data']['bonus']
        for row in range(len(bonus)):
            arr = (bonus[row]['ratio']).split(':')
            date = bonus[row]['date'].replace(', ', '-')
            bdsList.append(['bonus', date, str(date), arr[0], arr[1]])
    except:
        print("No bonus!")

    try:
        dividends = datajson['data']['dividends']
        for row in range(len(dividends)):
            arr = (dividends[row]['ratio']).split(' ')
            date = dividends[row]['date'].replace(', ', '-')
            bdsList.append(['dividends', date, str(date), arr[0], arr[1]])
    except:
        print("No dividends!")

    try:
        splits = datajson['data']['splits']
        for row in range(len(splits)):
            arr = (splits[row]['ratio']).split('-')
            date = splits[row]['date'].replace(', ', '-')
            bdsList.append(['splits', date, str(date), arr[0], arr[1]])
    except:
        print("No splits!")

    try:
        rights = datajson['data']['rights']
        for row in range(len(rights)):
            arr = (rights[row]['ratio']).split(':')
            date = rights[row]['date'].replace(', ', '-')
            bdsList.append(['rights', date, str(date), arr[0], arr[1]])
    except:
        print("No rights!")

    bdsdf = pd.DataFrame(
        bdsList, columns=['type', 'date', 'datestr', 'para1', 'para2'])
    bdsdf = bdsdf.sort_values(by='date')
    bdsdf.reset_index(inplace=True)

    stockunit = 10
    startUnit = stockunit
    facevalue = 10
    aList = []
    for row in range(len(bdsdf)):
        try:
            currentDate = str(bdsdf['datestr'][row])

            findRow = df.loc[df['datestr'].isin([currentDate])]

            resultrow = []
            if(len(findRow) > 0):
                i = findRow.index[0]
                resultrow = [currentDate, findRow['date']
                             [i], findRow['value'][i]]
            else:
                datetime_object = datetime.strptime(currentDate, '%Y-%M-%d')
                datearr = [(datetime_object - timedelta(days=1)).strftime("%Y-%M-%d"),
                           (datetime_object - timedelta(days=2)).strftime("%Y-%M-%d"),
                           (datetime_object - timedelta(days=3)).strftime("%Y-%M-%d")]
                findRow = df.loc[df['datestr'].isin(datearr)]
                print(findRow)
                i = findRow.index[(len(findRow)-1)]
                resultrow = [currentDate, findRow['date']
                             [i], findRow['value'][i]]

            dividend = 0
            if(bdsdf['type'][row] == 'splits'):
                stockunit = stockunit * \
                    (int(bdsdf['para1'][row]) / int(bdsdf['para2'][row]))
                facevalue = facevalue / \
                    (int(bdsdf['para1'][row]) / int(bdsdf['para2'][row]))
            elif (bdsdf['type'][row] == 'bonus'):
                stockunit = stockunit + \
                    (stockunit *
                     (int(bdsdf['para1'][row]) / int(bdsdf['para2'][row])))
            elif (bdsdf['type'][row] == 'dividends'):
                dividend = (float(bdsdf['para2'][row]) / 100) * stockunit
            elif (bdsdf['type'][row] == 'rights'):
                stockunit = stockunit + stockunit / \
                    (int(bdsdf['para2'][row]) / int(bdsdf['para1'][row]))

            aList.append([resultrow[0], resultrow[1], resultrow[2],
                          stockunit, facevalue, dividend])

            dfcal = pd.DataFrame(aList, columns=['currentDate', 'finddate', 'unitprice', 'stockunit', 'facevalue', 'dividend'])
            col = ['finddate', 'unitprice', 'stockunit', 'facevalue', 'dividend']
            bdsdf[col] = dfcal[col]
    
            investDate = df['date'][0]
            investValue = df['value'][0]
            investPrice = investValue * startUnit
    
            try:
                noUnit = bdsdf['stockunit'][len(bdsdf)-1]
            except:
                noUnit = startUnit
    
            todayValue = df['value'][len(df)-1]
            todayPrice = todayValue * noUnit
    
            try:
                totalDividend = dfcal['dividend'].sum()
            except:
                totalDividend = 0
    
            retrunTimes = todayPrice/investPrice
            retrunTimesDivd = (todayPrice + totalDividend) / investPrice
    
            resultList.append([cname, investDate, investValue, investPrice, facevalue, noUnit, todayValue, todayPrice,
                               totalDividend, retrunTimes, retrunTimesDivd, bdsdf])
        except:
            print('--> ' + cname)


dfResultList = pd.DataFrame(resultList, columns=['name', 'investDate', 'investValue', 'investPrice',
                                                 'facevalue', 'noUnit', 'todayValue', 'todayPrice',
                                                 'totalDividend', 'retrunTimes', 'retrunTimesDivd', 'bdsdf'
                                                 ])

# Writing to json file
with open("0CompPerform.json", "w") as outfile:
    outfile.write(dfResultList.to_json(orient='records', indent=4))
    
dfResultList.drop('bdsdf', axis=1, inplace=True)

