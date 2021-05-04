# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 16:20:29 2021

@author: Pritam

https://github.com/twopirllc/pandas-ta
pip install pandas-ta

https://reposhub.com/python/deep-learning/twopirllc-pandas-ta.html
"""
import os
import math
import numpy as np
import pandas as pd
import pandas_ta as ta
import json

fname = 'TCS'
df = pd.DataFrame(json.load(open('data/D/'+ fname +'.json')))

# List of all indicators
pd.DataFrame().ta.indicators()


# # Runs and appends all indicators to the current DataFrame by default
# # The resultant DataFrame will be large.
# df.ta.strategy()
# # Or equivalently use name='all'
# df.ta.strategy(name='all')

# df.ta.strategy(include=['bop', 'mom', 'percent_return', 'wcp', 'pvi'], verbose=True)

# # Sanity check. Make sure all the columns are there
print(df.columns)

# dfD['logR'] = dfD.ta.log_return(cumulative=True, append=True)
# dfD['percentR'] = dfD.ta.percent_return(cumulative=True, append=True)
# dfD['sma10'] = ta.sma(dfD.close, length=10)

# # print(df.ta.indicators())
