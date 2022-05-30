#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 30 17:40:20 2022

@author: pritamkhose

https://blog.jcharistech.com/2020/01/08/how-to-convert-json-to-sql-format-in-python/

pip install sqlite pandas sqlalchemy

https://www.sqlitetutorial.net/sqlite-dump/

sqlite> .output pincode.sql
sqlite> .dump
sqlite> .exit
"""

import pandas as pd
import json
import sqlite3
# Open JSON data
with open("/Users/pritamkhose/Documents/code/Dataset/pincode.json") as f:
    data = json.load(f)

# Create A DataFrame From the JSON Data
df = pd.DataFrame(data)

conn =sqlite3.connect("data.db")
c = conn.cursor()

df.to_sql("pincode2",conn)