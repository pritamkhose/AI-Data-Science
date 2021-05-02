# -*- coding: utf-8 -*-
"""
Created on Sat May  1 16:21:17 2021

@author: Pritam


"""

# Import the libraries
import os
import numpy as np
import pandas as pd
import json
import requests
from bs4 import BeautifulSoup, NavigableString, Tag

headers = {
    'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405', 'Host': 'www.moneycontrol.com'}


def getData():
    url = 'https://www.moneycontrol.com/stocks/marketinfo/marketcap/bse/index.html'
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    with open("mcbsehome.html", "w", encoding="utf-8") as file:
        file.write(str(soup.body))


def extractData():
    HtmlText = open("mcbsehome.html", 'r', encoding='utf-8').read()
    soup = BeautifulSoup(HtmlText, 'html.parser')
    aDiv = soup.find("div", {"class": "lftmenu"})
    aListURL = []
    for row in aDiv.findAll('a'):
        aListURL.append(row['href'])
    
    aData = []
    i = 0
    for row in aListURL:
        try:
            i += 1
            print(i, row)
            url = ("https://www.moneycontrol.com" + row)
            page = requests.get(url, headers=headers)
            soup = BeautifulSoup(page.content, 'html.parser')
            # with open("mcbsehome1.html", "w", encoding="utf-8") as file:
            #     file.write(str(soup.body))
            # HtmlText = open("mcbsehome1.html", 'r', encoding='utf-8').read()
            # soup = BeautifulSoup(HtmlText, 'html.parser')
            aTable = soup.find("table", {"class": "tbldata14 bdrtpg"})
            trrows = aTable.findAll('tr')
            trow = []
            for tr in trrows:
                ahref = tr.findAll('a')
                if(len(ahref) > 0):
                    link = ahref[0]
                    code = link['href'].split("/")
                    code = code[5]
                    aData.append([code, link.string, link['href'], row])
            mcFinal = pd.DataFrame(
                aData, columns=['mcCode', 'mcName', 'mcURL', 'industryURL'])
            mcFinal.to_json('mcbsehome.json', orient='records')
        except Exception as e:
            print(row, e)

def removeDuplicateData():
    source_df = pd.DataFrame(json.load(open('mcbsehome.json')))
    source_df.drop(['industryURL'], axis=1, inplace=True)
    result_df = source_df.drop_duplicates()
    result_df.to_json('mcbsehome1.json', orient='records')

