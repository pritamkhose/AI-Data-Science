#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 02 12:44:24 2022

@author: pritamkhose
"""

# Import the libraries
import os
import numpy as np
import pandas as pd


# res = pd.read_excel("NewEco.xlsx")


# https://www.ilovepdf.com/pdf_to_excel
# res = pd.read_excel("SYBA.xlsx")
# res = res.dropna(axis = 1, how = 'all')
# res = res.dropna(axis = 0, how = 'all')
# dfs = pd.read_excel("NewEco.xlsx", sheetname="Table 1")


from tabula import read_pdf
# df = read_pdf('SYBA.pdf', pages='all')
# dc = df[0].to_dict('split')

# PVList = []
# for x in range(0, len(df)):
#     PVList.append(df[x].to_dict('split')['columns'])
#     data = df[x].to_dict('split')['data']
#     for y in range(0, len(data)):
#         if(type(y) is list):
#             PVList.append(y)
    
# run output
PVList = []
for x in range(0, 17):
   data = pd.read_excel("output"+str(x)+".xlsx")
   # for y in range(0, len(data)):
   PVList.append(data)
   