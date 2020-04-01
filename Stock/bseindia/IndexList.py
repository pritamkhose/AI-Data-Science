# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 11:27:22 2020

@author: Pritam
https://www.bseindia.com/markets/equity/EQReports/MarketWatch.html?index_code=16

https://api.bseindia.com/BseIndiaAPI/api/IndexList/w
https://api.bseindia.com/bseindia/api/Sensex/getSensexData?json={%22fields%22:%221,2,3,4,5,6,7,8%22}
https://api.bseindia.com/BseIndiaAPI/api/SensexGraphData/w?index=98&flag=0&sector=&seriesid=R&frd=null&tod=null
https://api.bseindia.com/BseIndiaAPI/api/GetSensexDataN/w
https://api.bseindia.com/BseIndiaAPI/api/VolTopper/w?code=98
https://api.bseindia.com/BseIndiaAPI/api/HeatMapData/w?flag=HEAT&alpha=D&indexcode=98&random=1420201830



https://api.bseindia.com/BseIndiaAPI/api/getScripHeaderData/w?Debtflag=&scripcode=500325&seriesid=
https://api.bseindia.com/BseIndiaAPI/api/ComHeader/w?quotetype=EQ&scripcode=500325&seriesid=
https://api.bseindia.com/BseIndiaAPI/api/StockTrading/w?flag=&quotetype=EQ&scripcode=500325
https://api.bseindia.com/BseIndiaAPI/api/LeftMenu/w?quotetype=LMN&scripcode=500325
https://api.bseindia.com/BseIndiaAPI/api/HighLow/w?Type=EQ&flag=C&scripcode=500325
https://api.bseindia.com/BseIndiaAPI/api/PriceBand/w?scripcode=500325
https://api.bseindia.com/BseIndiaAPI/api/StockReachGraph/w?scripcode=500325&flag=0&fromdate=&todate=&seriesid=

https://api.bseindia.com/BseIndiaAPI/api/TabResults/w?scripcode=500325&tabtype=NEWS
https://api.bseindia.com/BseIndiaAPI/api/MarketDepth/w?flag=&quotetype=EQ&scripcode=500325
https://api.bseindia.com/BseIndiaAPI/api/EQPeerGp/w?scripcode=500325&scripcomare=
https://api.bseindia.com/BseIndiaAPI/api/TabResults/w?scripcode=500325&tabtype=RESULTS
https://api.bseindia.com/BseIndiaAPI/api/SecurityPosition/w?quotetype=EQ&scripcode=500325


https://realpython.com/beautiful-soup-web-scraper-python/
"""


#Import the libraries
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#plt.style.use('fivethirtyeight')
import json
import requests

# S%26P+BSE+SENSEX' S%26P+BSE+500  S%26P+BSE+AllCap
#url =  'https://api.bseindia.com/BseIndiaAPI/api/GetMktData/w?ordcol=TT&strType=index&strfilter=S%26P+BSE+AllCap'
url =  'https://api.bseindia.com/BseIndiaAPI/api/GetMktData/w?ordcol=TT&strType=AllMkt&strfilter=All'
datajson = (requests.get(url).json()['Table'])
#datainval = datajson['DataInputValues'][0]

if not os.path.exists('data'):
    os.makedirs('data')
# Writing to json file
with open('data/bseAll.json', 'w') as outfile: 
    outfile.write(json.dumps(datajson))