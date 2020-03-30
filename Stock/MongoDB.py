# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 11:27:22 2020

@author: Pritam

https://stackoverflow.com/questions/2817481/how-do-i-request-and-process-json-with-python
https://docs.atlas.mongodb.com/driver-connection/#driver-examples
python -m pip install numpy pandas matplotlib requests pymongo
"""


#Import the libraries
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
import requests
import pymongo
import dns  # required for connecting with SRV

URLArr = ['MPS', 'AP31', 'AB16', 'BAF', 'BF04', 'BA10', 'BA08', 'BI14', 'BI', 'BPC',
        'C', 'CI11', 'DRL', 'EM', 'GAI', 'GI01', 'HCL02', 'HDF', 'HDF01', 'HHM',
        'HI', 'HU', 'ICI02', 'IIB', 'IT', 'IOC', 'ITC', 'JSW01', 'KMB', 'LT',
        'MM', 'MS24', 'NI', 'NTP', 'ONG', 'PGC', 'RI', 'SBI', 'SC12', 'SPI',
        'TM03', 'TIS', 'TCS', 'TM4', 'TI01', 'UTC01', 'UP04', 'SG', 'W', 'ZEE',
        'HSL01', 'HAM02'];
dbname = 'moneycontrolchart'
dburl = 'mongodb://username:password@cluster0-shard-00-00-qhmqk.mongodb.net:27017,cluster0-shard-00-01-qhmqk.mongodb.net:27017,cluster0-shard-00-02-qhmqk.mongodb.net:27017/' + dbname + '?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true'
client = pymongo.MongoClient(dburl)

#i = 'SBI'
for i in URLArr:
    #Get the stock quote
    url = 'https://www.moneycontrol.com/mc/widget/basicchart/get_chart_value?dur=max&sc_did=' + i
    data = requests.get(url).json()
    data.update({'id': i})
    collection = client.moneycontrolchart[i]
    collection.drop()
    collection.insert_one(data)
    print(i)

##Save the stock quote chart in single ChartAll Collection
#collection = client.moneycontrol.ChartAll
#collection.drop()          
#for i in URLArr[0:5]:
#    #Get the stock quote
#    url = 'https://www.moneycontrol.com/mc/widget/basicchart/get_chart_value?dur=max&sc_did=' + i
#    data = requests.get(url).json()
#    data.update({'id': i})
#    collection.insert_one(data)
#    print(i)

##Get the stock quote
#collection = client.moneycontrol.ChartAll 
#result_cur = collection.find()
#x =[]
#x = []
#for i in result_cur:
#    x.append(i)