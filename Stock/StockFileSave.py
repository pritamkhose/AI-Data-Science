# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 11:27:22 2020

@author: Pritam

https://stackoverflow.com/questions/2817481/how-do-i-request-and-process-json-with-python
https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/
python -m pip install numpy pandas matplotlib requests pymongo
"""


#Import the libraries
import os
import json
import math
import numpy as np
import pandas as pd
import requests

if not os.path.exists('data'):
    os.makedirs('data')

URLArr = ['MPS', 'AP31', 'AB16', 'BAF', 'BF04', 'BA10', 'BA08', 'BI14', 'BI', 'BPC',
        'C', 'CI11', 'DRL', 'EM', 'GAI', 'GI01', 'HCL02', 'HDF', 'HDF01', 'HHM',
        'HI', 'HU', 'ICI02', 'IIB', 'IT', 'IOC', 'ITC', 'JSW01', 'KMB', 'LT',
        'MM', 'MS24', 'NI', 'NTP', 'ONG', 'PGC', 'RI', 'SBI', 'SC12', 'SPI',
        'TM03', 'TIS', 'TCS', 'TM4', 'TI01', 'UTC01', 'UP04', 'SG', 'W', 'ZEE',
        'HSL01', 'HAM02'];

for i in URLArr:
    #Get the stock quote
    url = 'https://www.moneycontrol.com/mc/widget/basicchart/get_chart_value?dur=max&sc_did=' + i
    data = requests.get(url).json()
    data.update({'id': i})
    # Writing to json file
    with open('data/'+i+'.json', 'w') as outfile: 
        outfile.write(json.dumps(data))
    print(i)