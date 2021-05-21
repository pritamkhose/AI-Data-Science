# -*- coding: utf-8 -*-
"""
Created on Tue May 18 12:52:13 2021

@author: Pritam

https://archives.nseindia.com/corporate/xbrl/SHP_157001_434730_14042021091358_WEB.xml

https://archives.nseindia.com/corporate/xbrl/IT_1099600_448537_17052021100130_WEB.xml
"""

# Import lib
from datetime import datetime
import os
import json
import requests
import xmltodict
from flask import jsonify

data = open('C:/Users/Pritam/Downloads/SHP_157001_434730_14042021091358_WEB.xml', 'r').read()
body = xmltodict.parse(data)

json.dump(body, open('result.json', 'w'))
    