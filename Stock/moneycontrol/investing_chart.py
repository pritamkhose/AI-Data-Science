# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 11:27:22 2020

@author: Pritam
https://www.investing.com/equities/infosys-chart?cid=39538

https://tvc6.forexpros.com/089b37fc411617093ef56d9b70fa3a9c/1587877206/1/1/8/history?symbol=39538&resolution=1&from=1587635940&to=1587635940
https://tvc6.forexpros.com/089b37fc411617093ef56d9b70fa3a9c/1587877206/1/1/8/history?symbol=39538&resolution=1&from=1587715197&to=1587722339
https://tvc6.forexpros.com/089b37fc411617093ef56d9b70fa3a9c/1587877206/1/1/8/history?symbol=39538&resolution=D&from=1556773232&to=1587877292
https://tvc6.forexpros.com/089b37fc411617093ef56d9b70fa3a9c/1587877206/1/1/8/history?symbol=39538&resolution=M&from=1276837569&to=1587877629
https://tvc6.forexpros.com/089b37fc411617093ef56d9b70fa3a9c/1587877206/1/1/8/history?symbol=39538&resolution=W&from=1494565592&to=1587877652
https://tvc6.forexpros.com/089b37fc411617093ef56d9b70fa3a9c/1587877206/1/1/8/history?symbol=39538&resolution=60&from=1587272893&to=1587877753
https://tvc6.forexpros.com/089b37fc411617093ef56d9b70fa3a9c/1587877206/1/1/8/history?symbol=39538&resolution=15&from=1587683484&to=1587721499


https://tvc6.forexpros.com/089b37fc411617093ef56d9b70fa3a9c/1587877206/1/1/8/marks?symbol=39538&from=1557114300&to=2114361000&resolution=W
"""


#Import the libraries
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#plt.style.use('fivethirtyeight')
import json
import requests
# infy 39538
url = 'https://tvc6.forexpros.com/089b37fc411617093ef56d9b70fa3a9c/1587877206/1/1/8/history?symbol=39538&resolution=1&from=1587635940&to=1587635940'
datajson = requests.get(url)
print(datajson)
