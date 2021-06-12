# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 18:54:22 2021

@author: Pritam

# pip install bs4

Job run on https://gitpod.io/
python --version
python ListCompanies11.py
"""

# Import the libraries
import os
import json
import requests
from bs4 import BeautifulSoup, NavigableString, Tag

headers = {'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405', 'Host': 'www.moneycontrol.com'}

def getData():
    CompArr = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'OTHERS']
    aListURL = []
    for x in CompArr:
        print(x)
        url = 'https://www.moneycontrol.com/india/stockpricequote/' + x
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        # with open("CompArr_A.html", "w", encoding="utf-8") as file:
        #     file.write(str(soup.body))
        # HtmlText = open("CompArr_A.html", 'r', encoding='utf-8').read()
        # soup = BeautifulSoup(HtmlText, 'html.parser')
        aDiv = soup.find("table", {"class": "pcq_tbl MT10"})
        for row in aDiv.findAll('a'):
            if(row['href'] != ''):
                aListURL.append({'mcName': row.string, 'mcURL': row['href']})
    with open('mcCompAllA-Z.json', 'w', encoding='utf-8') as f:
        json.dump(aListURL, f, ensure_ascii=False, indent=2)
    return aListURL

print(headers)

def getComp(CompArr):
    aResult = []
    for x in CompArr:
        try:
            print(x['mcName'])
            url = x['mcURL']
            page = requests.get(url, headers=headers)
            soup = BeautifulSoup(page.content, 'html.parser')
            aboutComp = soup.find("ul", {"class": "comp_inf company_slider"})
            a = aboutComp.findChildren("li" , recursive=False)
            a = a[4].findChildren("p")
            urlspilt = url.split("/")
            x['mcCode']= urlspilt[7]
            x['BSE']= a[0].text
            x['NSE']= a[1].text
            x['ISIN']= a[3].text
            aResult.append(x)
        except Exception as e:
            print(x['mcName'], e)
    with open('mcCompAllA-ZData.json', 'w', encoding='utf-8') as f:
        json.dump(aResult, f, ensure_ascii=False, indent=2)
    return aResult

# aListURL = getData()
# aResult = getComp([0:30])
aListURL = json.load(open('mcCompAllA-Z.json'))
aResult = getComp(aListURL)