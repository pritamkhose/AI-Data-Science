# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 20:32:32 2020

@author: Pritam

https://in.finance.yahoo.com/quote/%5EBSESN/chart?p=%5EBSESN

https://query1.finance.yahoo.com/v8/finance/chart/%5EBSESN?symbol=%5EBSESN&period1=1587395612&period2=1587914012&interval=1m&includePrePost=true&events=div%7Csplit%7Cearn&lang=en-IN&region=IN&crumb=5VF6S%2Fpyqty&corsDomain=in.finance.yahoo.com

https://query1.finance.yahoo.com/v8/finance/chart/INFY.BO?symbol=INFY.BO
https://query1.finance.yahoo.com/v8/finance/chart/INFY.BO?symbol=INFY.BO&period1=946665000&period2=1587959100&interval=1d


https://query1.finance.yahoo.com/v8/finance/chart/INFY.BO?region=IN&lang=en-IN&includePrePost=false&interval=30m&range=1mo
https://query1.finance.yahoo.com/v8/finance/chart/INFY.BO?region=IN&lang=en-IN&includePrePost=false&interval=1d&range=1y
https://query1.finance.yahoo.com/v8/finance/chart/INFY.BO?region=IN&lang=en-IN&includePrePost=false&interval=15m&range=5d
https://query1.finance.yahoo.com/v8/finance/chart/INFY.BO?region=IN&lang=en-IN&includePrePost=false&interval=2m&range=1d

https://query1.finance.yahoo.com/v8/finance/chart/INFY.BO?region=IN&lang=en-IN&includePrePost=false&interval=1m&range=5d

https://query2.finance.yahoo.com/v10/finance/quoteSummary/ICICIBANK.NS?formatted=true&lang=en-IN&region=IN&modules=summaryProfile%2CfinancialData%2CrecommendationTrend%2CupgradeDowngradeHistory%2Cearnings%2CdefaultKeyStatistics%2CcalendarEvents%2CesgScores%2Cdetails
https://query2.finance.yahoo.com/v10/finance/quoteSummary/SBICARD.NS?formatted=true&lang=en-IN&region=IN&modules=summaryProfile%2CfinancialData%2CrecommendationTrend%2CupgradeDowngradeHistory%2Cearnings%2CdefaultKeyStatistics%2CcalendarEvents%2CesgScores%2Cdetails
"""



#Import the libraries
import os
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#plt.style.use('fivethirtyeight')
import json
import requests
from datetime import datetime

#1d 5d max
compname = ''
url = 'https://query1.finance.yahoo.com/v8/finance/chart/INFY.BO?region=IN&lang=en-IN&includePrePost=false&interval=1m&range=5d'
datajson = requests.get(url).json()

df = pd.DataFrame(list(zip(datajson['chart']['result'][0]['timestamp'], 
                           datajson['chart']['result'][0]['indicators']['quote'][0]['open'], 
                           datajson['chart']['result'][0]['indicators']['quote'][0]['close'],
                           datajson['chart']['result'][0]['indicators']['quote'][0]['low'],
                           datajson['chart']['result'][0]['indicators']['quote'][0]['high'],
                           datajson['chart']['result'][0]['indicators']['quote'][0]['volume'] )), 
               columns =['timestamp', 'open', 'close', 'low', 'high', 'volume'])
df = df[df['open'].notna()]

df['timestamp'] = [str(datetime.fromtimestamp(x)) for x in df['timestamp']]

if not os.path.exists('data'):
    os.makedirs('data')
# Writing to json file
df.to_json('data/'+compname + '1.json', orient='records')