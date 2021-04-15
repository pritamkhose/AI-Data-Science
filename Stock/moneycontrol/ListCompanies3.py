# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 09:05:41 2021

@author: Pritam

https://www.moneycontrol.com/mccode/common/autosuggestion_solr.php?classic=true&query=i&type=1&format=json

"""


# Import the libraries
import os
import numpy as np
import pandas as pd
import json
import requests

charset = 'abcdefghijklmnopqrstuvwxyz0123456789'
filePath = 'searchdata/'


def getData():
    mcurl = 'https://www.moneycontrol.com/mccode/common/autosuggestion_solr.php?classic=true&query='
    urlpost = '&type=1&format=json'
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405',
        'Host': 'www.moneycontrol.com'
    }

    if not os.path.exists(filePath):
        os.makedirs(filePath)
    # charset = '90'
    for i in range(len(charset)):
        url = mcurl + str(charset[i]) + urlpost
        print(url)
        # dataObj = requests.get(url , headers=headers).json()
        # with open(filePath + str(charset[i]) + '.json', 'w') as fp:
        #     json.dump(dataObj, fp)

# getData()


def getLocalData():
    PVList = []
    for i in range(len(charset)):
        fdata = json.load(open(filePath + str(charset[i]) + '.json'))
        for row in fdata:
            PVList.append(row)
    mcdf = pd.DataFrame(PVList, columns=[
                        'link_src', 'pdt_dis_nm', 'sc_id', 'stock_name', 'sc_sector', 'sc_sector_id'])
    mcdf = mcdf.rename(columns={'pdt_dis_nm': 'pdt'})
    mcdf['lsn'] = mcdf['pdt'].str.split("&nbsp;")
    return mcdf


mcdf = getLocalData()
mcdf['i'] = mcdf.index
# duplicateRowsDF = mcdf[mcdf.duplicated(['sc_id'])]

PVList = []
for i in range(len(mcdf)):
    a = mcdf['lsn'][i][1]
    a = a.replace("<span>", "")
    a = a.replace("</span>", "")
    b = a.split(", ")
    if(len(b) == 2):
        b.insert(1, '')
    b.insert(0, i)
    PVList.append(b)
resultdf = pd.DataFrame(PVList, columns=['i', 'INE', 'mc', 'scrip_cd'])

# bigdata = mcdf.append(resultdf)
resultlsn = pd.merge(mcdf, resultdf, how='inner', on='i')
