# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 11:27:22 2020

@author: Pritam

"""

# Import the libraries
import os
import math
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

import json
import requests


compname = 'IT' #SBI TCS W HDF01 SBI HDF01

# Get Data #1d 5d max
url = 'https://www.moneycontrol.com/mc/widget/basicchart/get_chart_value?classic=true&dur=max&sc_did=' + compname
datajson = requests.get(url).json()

if not os.path.exists('data'):
    os.makedirs('data')
# Writing to json file
with open('data/'+compname + '.json', 'w') as outfile:
    outfile.write(json.dumps(datajson))

# Read to json file
with open('data/'+compname + '.json') as json_file:
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
    currentDate = str(bdsdf['datestr'][row])

    findRow = df.loc[df['datestr'].isin([currentDate])]

    resultrow = []
    if(len(findRow) > 0):
        i = findRow.index[0]
        resultrow = [currentDate, findRow['date'][i], findRow['value'][i]]
    else:
        datetime_object = datetime.strptime(currentDate, '%Y-%M-%d')
        datearr = [(datetime_object - timedelta(days=1)).strftime("%Y-%M-%d"),
                   (datetime_object - timedelta(days=2)).strftime("%Y-%M-%d"),
                   (datetime_object - timedelta(days=3)).strftime("%Y-%M-%d")]
        findRow = df.loc[df['datestr'].isin(datearr)]
        i = findRow.index[(len(findRow)-1)]
        resultrow = [currentDate, findRow['date'][i], findRow['value'][i]]

    dividend = 0
    if(bdsdf['type'][row] == 'splits'):
        stockunit = stockunit * \
            (int(bdsdf['para1'][row]) / int(bdsdf['para2'][row]))
        facevalue = facevalue / \
            (int(bdsdf['para1'][row]) / int(bdsdf['para2'][row]))
    elif (bdsdf['type'][row] == 'bonus'):
        stockunit = stockunit + \
            (stockunit * (int(bdsdf['para1'][row]) / int(bdsdf['para2'][row])))
    elif (bdsdf['type'][row] == 'dividends'):
        dividend = (float(bdsdf['para2'][row]) / 100) * stockunit
    elif (bdsdf['type'][row] == 'rights'):
        stockunit = stockunit + stockunit / \
            (int(bdsdf['para2'][row]) / int(bdsdf['para1'][row]))

    aList.append([resultrow[0], resultrow[1], resultrow[2],
                  stockunit, facevalue, dividend])


dfcal = pd.DataFrame(aList, columns=[
                     'currentDate', 'finddate', 'unitprice', 'stockunit', 'facevalue', 'dividend'])
col = ['finddate', 'unitprice', 'stockunit', 'facevalue', 'dividend']
bdsdf[col] = dfcal[col]

totalDividend = dfcal['dividend'].sum()
print('Total Divident = ₹ ' + str(totalDividend))
noUnit = bdsdf['stockunit'][len(bdsdf)-1]
print('No. of Stocks = ' + str(noUnit) + ' No.s')
print('Invest Date = ' + str(df['date'][0]))
investPrice = df['value'][0]
print('Invest Rate = ₹ ' + str(investPrice))
print('Invest Price = ' + str(startUnit * investPrice))
todayPrice = df['value'][len(df)-1]
print('Current Rate = ' + str(todayPrice))
print('Current Price = ₹ ' + str(noUnit * todayPrice))
print('Retrun = ' + str((noUnit * todayPrice)/(startUnit * investPrice)) + ' times')
print('Retrun with Divident = ' + str((totalDividend +
                                       (noUnit * todayPrice))/(startUnit * investPrice)) + ' times')
