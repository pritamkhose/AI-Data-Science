# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 19:01:56 2020

@author: Pritam
"""
#Import the libraries
import os
import math
import numpy as np
import pandas as pd

no_of_year = 15
rate = 7.5
depositAmt = 150000
tempAmt = 0
interest = 0
totalInterest = 0

tempAmt = depositAmt;

PVList=[]
for x in range(no_of_year):
  interest = (tempAmt * rate )/ 100
  tempAmt += depositAmt + interest
  totalInterest+= interest
  PVList.append([x+1, depositAmt, interest, tempAmt, totalInterest])

df = pd.DataFrame(PVList, columns =['year', 'depositAmt', 'interest', 'tempAmt', 'totalInterest'])
