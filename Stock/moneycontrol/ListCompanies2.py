# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 09:05:41 2021

@author: Pritam

https://www.moneycontrol.com/markets/indian-indices/top-bse-500-companies-list/12?classic=true
https://www.moneycontrol.com/markets/indian-indices/top-bseallcap-companies-list/67?classic=true

"""


# Import the libraries
import os
import numpy as np
import pandas as pd
import json
import requests
from bs4 import BeautifulSoup, NavigableString, Tag


def getMCComp():
    mcurl = 'https://www.moneycontrol.com/markets/indian-indices/top-bseallcap-companies-list/67?classic=true'
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405',
        'Host': 'www.moneycontrol.com'
    }
    page = requests.get(mcurl, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    trow = getTableData(soup, "div", "class", "indices")

    PVList = []
    for row in trow:
        urlspilt = row[1][1].split("/")
        code = urlspilt[7]
        industry = urlspilt[5].replace('-', ' ')
        PVList.append(
            {'mcName': row[1][0], 'mcURL': row[1][1], 'mcCode': code, 'mcIndustry': industry})
    mcdf = pd.DataFrame(
        PVList, columns=['mcName', 'mcURL', 'mcCode', 'mcIndustry'])
    mcdf.to_json('mcbseAll.json', orient='records')
    return mcdf


def getTableData(soup, divName, classId, classIdName):
    aDiv = soup.find(divName, {classId: classIdName})
    aTable = aDiv.find("table")
    trrows = aTable.tbody.findAll('tr')
    trow = []
    for tr in trrows:
        i = 0
        tdata = []
        for temprow in tr:
            tdList = []
            if(type(temprow) == Tag):
                dataname = []
                if(i == 0):
                    tdList.append(temprow.text)
                    for link in temprow.findAll("a"):
                        tdList.append(str(link.get("href")))
                else:
                    tdList.append(temprow.text)
                i += 1
            tdata.append(tdList)
        trow.append(tdata)
    return trow
