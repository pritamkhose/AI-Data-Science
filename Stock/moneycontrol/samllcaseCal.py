# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 12:28:10 2021

@author: Pritam

Smallcase IT Sector
"""

# Import the libraries
import os
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# plt.style.use('fivethirtyeight')
import json
import requests

# Read to json file
with open('SmallCaseComp.json') as json_file:
    compjson = json.load(json_file)

# Get Data from API - 1d 5d max
# for x in compjson:
#     print(x)
#     compname = x["mccode"]
#     url = 'https://www.moneycontrol.com/mc/widget/basicchart/get_chart_value?classic=true&dur=max&sc_did=' + compname
#     datajson = requests.get(url).json()

#     if not os.path.exists('data'):
#         os.makedirs('data')
#     # Writing to json file
#     with open('data/'+compname + '.json', 'w') as outfile:
#         outfile.write(json.dumps(datajson))

# Convert Data
percentTotal = 0
lastPriceTotal = 0
ago1YPriceTotal = 0
resultList = []

for x in compjson:
    resultDict = {}
    compname = x["mccode"]
    percentTotal += x["wt"]
    # Read to json file
    with open('data/'+compname + '.json') as json_file:
        stock = json.load(json_file)['g1']

    PVList = []
    for row in range(len(stock)):
        PVList.append([stock[row]['date'],
                       float(stock[row]['open']), float(stock[row]['close']),
                       float(stock[row]['low']), float(stock[row]['high']),
                       float(stock[row]['volume'])
                       ])
    df = pd.DataFrame(PVList, columns=['date', 'O', 'C', 'L', 'H', 'Vol'])
    dflen = len(df)-1
    lastPriceTotal += df['C'][dflen]
    ago1YPriceTotal += df['C'][dflen-25]
    resultDict = [x["mccode"], x["wt"], df['C'][dflen], df['C'][dflen-250], df]
    resultList.append(resultDict)
print("percentTotal = " + str(percentTotal))
print("lastPriceTotal = " + str(lastPriceTotal))
print("ago1YPriceTotal = " + str(ago1YPriceTotal))

# Find Max stock
maxStockPrice = 0
oneUnitPercPrice = 0
maxStock = []
for x in resultList:
    if(maxStockPrice < x[2]):
        maxStockPrice = x[2]
        maxStock = [x[0], x[1], x[2]]
        oneUnitPercPrice = x[2] / x[1]
print("maxStock = " + str(maxStock) + str(oneUnitPercPrice))

# Find Qty
aList = []
totalpay = 0
for x in resultList:
    calperprice = oneUnitPercPrice * x[1]
    unitqtyround = round(calperprice / x[2], 0)
    priceQty = [x[0], x[1], x[2], calperprice,
                unitqtyround, unitqtyround * x[2]]
    aList.append(priceQty)
    totalpay += unitqtyround * x[2]

# Calculate Current Price
print("totalpay = " + str(totalpay))
bList = []
for x in aList:
    bList.append([x[0], x[5], x[4], x[1], x[5]*100/totalpay])
dfResult = pd.DataFrame(
    bList, columns=['code', 'price', 'qty', 'fivenPer', 'currentPer'])

cList = []
# plot graph
for x in resultList:
    col = x[4]['C']
    collen = len(col)-1
    colSelect = col[collen-250:collen]
    cList.append(colSelect)

dList = []
for i in range(250):
    print(i)
    # for idx, val in enumerate(cList):
    #     print(val)
