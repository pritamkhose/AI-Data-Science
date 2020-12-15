# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 12:47:06 2020

@author: Pritam


"""

import requests
from bs4 import BeautifulSoup
import os
import math
import numpy as np
import pandas as pd
import json


with pd.HDFStore('./FullData.h5') as hdf:
    # This prints a list of all group names:
    FullDataKeys = hdf.keys()

df = pd.read_hdf('./FullData.h5', key='/INFY__EQ__NSE__NSE__MINUTE')
df.to_json('infy.json')

# df_wipro = pd.read_hdf('./FullData.h5', key='/WIPRO__EQ__NSE__NSE__MINUTE')
# df_wipro.to_json('WIPRO.json')
