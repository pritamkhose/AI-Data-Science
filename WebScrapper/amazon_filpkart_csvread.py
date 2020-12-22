# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 22:09:28 2020

@author: Pritam

amazon_co-ecommerce_sample.csv
flipkart_com-ecommerce_sample.csv
"""

import requests
from bs4 import BeautifulSoup
import os
import math
import numpy as np
import pandas as pd
import json
from pathlib import Path
path = Path(os.path.dirname(os.path.realpath(__file__)))

fname = "flipkart_com-ecommerce_sample"

df = pd.read_csv(fname + ".csv")


df = df[0:10]

for index, row in df.iterrows():
    pline = row.product_category_tree[2:-2]
    pline = pline.replace(" >> ", "/").replace("'", "").replace(" ", "+").split(",+")
    df.product_category_tree[index]= pline
    df.product_specifications[index]= json.loads(row.product_specifications.replace("=>", ":"))

# Writing to json file
with open(fname + '.json', 'w') as outfile:
    outfile.write(df.to_json(orient='index', indent=2))