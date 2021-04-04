# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 09:05:41 2021

@author: Pritam

https://www.bseindia.com/eqstreamer/StreamerMarketwatch.html?flag=1

https://www.moneycontrol.com/markets/indian-indices/top-bse-500-companies-list/12?classic=true

download CSV
https://www.nseindia.com/products-services/indices-nifty500-index

https://www.bseindia.com/corporates/List_Scrips.aspx
"""


#Import the libraries
import os
import numpy as np
import pandas as pd
import json
import requests
from bs4 import BeautifulSoup, NavigableString, Tag


def getBSEComp():
    headers = { 'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",}
    url =  'https://api.bseindia.com/BseIndiaAPI/api/GetStkCurrMain/w?flag=Equity&ddlVal1=Index&ddlVal2=S%26P%20BSE%20500&m=0&pgN='
    
    PVList = []
    for x in range(1,18):
      datajson = requests.get((url + str(x)), headers=headers).json()
      for row in range(len(datajson)):
          PVList.append([datajson[row]['Symbol'], datajson[row]['ScripName'], datajson[row]['LongName'], datajson[row]['URL']])
    # "ATP", "Open", "High", "Low", "PreCloseRate", "PercentChange", "upperCircuit", "lowerCircuit", "Wk52High", "W2AvgQ" , "Wk52low", "MCapFF", "MCapFull"
    
    bsedf = pd.DataFrame(PVList, columns =['scrip_cd','scripname', 'name', 'url']) 
    bsedf.to_json('bse500.json', orient='records')


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

def getMCComp():
    mcurl =  'https://www.moneycontrol.com/markets/indian-indices/top-bse-500-companies-list/12?classic=true'
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
        PVList.append({'mcName': row[1][0], 'mcURL': row[1][1], 'mcCode': code, 'mcIndustry': industry})
    mcdf = pd.DataFrame(PVList, columns =['mcName','mcURL', 'mcCode', 'mcIndustry']) 
    mcdf.to_json('mc500.json', orient='records')


def getCompare():
    bseDF = pd.DataFrame(json.load(open('bse500.json')))
    bseDF = bseDF.sort_values(by=['name'], ascending=True)
    bseDF = bseDF.reset_index(drop=True)
    
    mcDF = pd.DataFrame(json.load(open('mc500.json')))
    mcDF = mcDF.sort_values(by=['mcName'], ascending=True)
    mcDF = mcDF.reset_index(drop=True)
    
    aList =[]
    for bserow in range(len(bseDF)):
        for mcrow in range(len(mcDF)):
            if(mcDF['mcName'][mcrow].lower() in bseDF['name'][bserow].lower()):
                # print(bseDF['name'][bserow], mcDF['mcName'][mcrow])
                # aList.append([bserow, mcrow, bseDF.iloc[bserow], mcDF.iloc[mcrow]])
                bse = bseDF.iloc[bserow]
                mc = mcDF.iloc[mcrow]
                aList.append([bserow, mcrow, 
                              bse['scrip_cd'], bse['scripname'],  bse['name'], bse['url'], 
                              mc['mcName'], mc['mcURL'],  mc['mcCode'], mc['mcIndustry']])
                break
    resultdf = pd.DataFrame(aList, columns =['bsei', 'mci','scrip_cd', 'scripname', 'name', 'url', 'mcName','mcURL', 'mcCode', 'mcIndustry']) 
    
    # duplicateRowsDF = resultdf[resultdf.duplicated(['scrip_cd'])]  
    duplicateRowsDF = resultdf[resultdf.duplicated(['mcCode'])]  
    resultdf.drop_duplicates(subset ="scrip_cd", keep ='first', inplace = True)
    resultdf.drop(['bsei', 'mci'], axis=1, inplace=True)
    # resultdf['scrip_cd'] = (resultdf['scrip_cd']).astype(int)
    
    resultdf.to_json('result500.json', orient='records')
    
    
    idlist = (resultdf.scrip_cd).tolist()
    bseFilter = bseDF[~bseDF["scrip_cd"].isin(idlist)]
    bseFilter['scrip_cd'] = (bseFilter['scrip_cd']).astype(int)
    bseFilter.to_json('bseFilter.json', orient='records')
    
    mclist = (resultdf.mcCode).tolist()
    mcFilter = mcDF[~mcDF["mcCode"].isin(mclist)]
    mcFilter.to_json('mcFilter.json', orient='records')

def AfterEdit():
    resultDF = pd.DataFrame(json.load(open('result500Edit.json')))
    resultDF['scrip_cd'] = (resultDF['scrip_cd']).astype(int)
    resultDF = resultDF.sort_values(by=['scripname'], ascending=True)
    resultDF.to_json('result500Final.json', orient='records')
 
# def nseGet()
# nsedf = pd.read_csv("ind_nifty500list.csv")
# aList =[]
# for resultrow in range(len(resultDF)):
#     for nserow in range(len(nsedf)):
#         if(resultDF['name'][resultrow].lower() in nsedf['Company Name'][nserow].lower()):
#             a = resultDF.iloc[resultrow].tolist()
#             a.append(resultrow)
#             a.append(nserow)
#             b = nsedf.iloc[resultrow].tolist()
#             aList.append(a+b)

# def BSENSEMerge():
nsedf = pd.read_csv("ind_nifty500list.csv")
nsedf.drop(['Series'], axis=1, inplace=True)
nsedf = nsedf.rename(columns={'ISIN Code': 'ISIN', 'Company Name': 'nseName', 'Symbol': 'nseCode', 'Industry': 'nseIndustry'})
nsedf = nsedf.rename(columns={})

bsedf = pd.read_csv("bseEquity.csv")
bsedf = bsedf.rename(columns={'Security Code': 'scrip_cd', 'Security Name': 'name', 'Security Id': 'scripname', 'Industry': 'bseIndustry', 'Face Value': 'bseFV'})
bsedf.drop(['Issuer Name', 'Group', 'Status', 'Instrument'], axis=1, inplace=True)
bsedf = bsedf.rename(columns={'ISIN No': 'ISIN'})
resultBSENSE = pd.merge(bsedf, nsedf, how ='inner', on ='ISIN')
resultBSENSE.drop(['name', 'scripname'], axis=1, inplace=True)

resultDF = pd.DataFrame(json.load(open('result500Final.json')))

resultBSENSEMC = pd.merge(resultDF, resultBSENSE, how ='inner', on ='scrip_cd')
resultBSENSEMC.to_json('result500BSENSEMC.json', orient='records')
