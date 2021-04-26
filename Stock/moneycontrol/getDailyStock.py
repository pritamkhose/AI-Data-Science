# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 17:00:28 2021

@author: Pritam
"""

from datetime import datetime
import os
import math
import numpy as np
import pandas as pd
import json
import requests

x = 'data'
if not os.path.exists(x):
    os.makedirs(x)

companyName = pd.DataFrame(
    json.load(open('E:\Code\python\Stock\StockAPI\extra\stock_bse_nse_mc.json')))

headers = {
    'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405',
    'Host': 'www.moneycontrol.com'
}
url = 'https://www.moneycontrol.com/mc/widget/basicchart/get_chart_value?sc_did='

for row in companyName["mc_code"]:
    print(row)
    data = requests.get(url + row + '&dur=max', headers=headers).json()
    json.dump(data, open('data/' + row + '.json', 'w'))
