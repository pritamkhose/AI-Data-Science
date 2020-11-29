# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 11:19:22 2020

@author: Pritam

https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_hdf.html
"""

import requests
from bs4 import BeautifulSoup
import os
import math
import numpy as np
import pandas as pd
import json


# df = pd.DataFrame([[1, 1.0, 'a']], columns=['x', 'y', 'z'])
# df.to_hdf('./store.h5', 'data')
# reread = pd.read_hdf('./store.h5')


with pd.HDFStore('./FullData.h5') as hdf:
    # This prints a list of all group names:
    FullDataKeys = hdf.keys()

df = pd.read_hdf('./FullData.h5', key='/INFY__EQ__NSE__NSE__MINUTE')

# with open('infy' + '.json', 'w') as outfile:
#     outfile.write(json.dumps(df))

df.to_json('infy.json')