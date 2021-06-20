# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 20:01:30 2021

@author: Pritam

download CSV
nse 
https://www.nseindia.com/products-services/indices-nifty500-index
https://www.nseindia.com/regulations/listing-compliance/nse-market-capitalisation-all-companies
https://www.nseindia.com/all-reports  BhavcopyCSV

bse
https://www.bseindia.com/corporates/List_Scrips.aspx

"""


# Import the libraries
import os
import numpy as np
import pandas as pd
import json
import requests
from bs4 import BeautifulSoup, NavigableString, Tag

headers = {
    'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405',
    'Host': 'www.moneycontrol.com'
}


def getDataURL():
    mcurl = 'https://www.moneycontrol.com/india/stockpricequote/computers-software/tataconsultancyservices/TCS'

    page = requests.get(mcurl, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    with open("TCS1.html", "w", encoding="utf-8") as file:
        file.write(str(soup.body))


def getDataAllCapURLHTML():
    mcList = json.load(open('mcbseAll.json'))
    # if Files miss to create
    # mcdf = pd.DataFrame(mcList)
    # mcMiss = (mcdf.loc[mcdf['mcCode'].isin(['SBI','HUD', 'JL'])])
    # mcMiss.to_json('mcMiss.json', orient='records')
    # mcList = json.load(open('mcMiss.json'))
    if not os.path.exists('dataINE/'):
        os.makedirs('dataINE/')
    for row in mcList:
        print(row['mcCode'], row['mcURL'])
        page = requests.get(row['mcURL'], headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        with open('dataINE/' + row['mcCode'] + ".html", "w", encoding="utf-8") as file:
            file.write(str(soup.body))
# getDataAllCapURLHTML()


def calculateAllCapURLHTML():
    mcList = json.load(open('mcbseAll.json'))
    PVList = []
    for row in mcList:  # mcList[0:2]
        try:
            mrow = row
            htmlStr = open('dataINE/' + row['mcCode'] +
                           ".html", "r", encoding="utf-8").read()
            soup = BeautifulSoup(htmlStr, 'html.parser')
            aUl = soup.findAll("ul", {"class": "comdetl"})
            aLi = aUl[(len(aUl)-1)].findAll("li", {"class": "clearfix"})
            mrow['bseCode'] = int(aLi[0].find('p').text)
            mrow['nseCode'] = aLi[1].find('p').text
            mrow['ISIN'] = str(aLi[3].find('p').text)
            PVList.append(mrow)
        except:
            print(row['mcCode'])
    mcFinal = pd.DataFrame(PVList, columns=[
                           'bseCode', 'ISIN', 'mcCode', 'mcIndustry', 'mcName', 'mcURL', 'nseCode'])
    mcFinal.to_json('mcbseAllCapScript.json', orient='records')


def mergeResult():
    mcdfAllCap = pd.DataFrame(json.load(open('mcbseAllCapScript.json')))
    resultBSENSE = pd.DataFrame(json.load(open('resultBSENSE.json')))
    resultBSENSE = resultBSENSE.rename(columns={'pdt_dis_nm': 'pdt'})

    resultMCBSENSE = pd.merge(mcdfAllCap, resultBSENSE, how='inner', on='ISIN')
    print(resultMCBSENSE.columns)
    # resultMCBSENSE['compareBSE'] = resultMCBSENSE['bseCode'] == resultMCBSENSE['Security Code']
    resultMCBSENSE['compareNSE'] = resultMCBSENSE['nseCode'] == resultMCBSENSE['SYMBOL']

    resultMCBSENSE.drop(['SYMBOL', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'LAST', 'PREVCLOSE', 'Security Code',
                         'TOTTRDQTY', 'TOTTRDVAL', 'TOTALTRADES', 'Instrument', 'compareNSE'], axis=1, inplace=True)

    duplicateRowsDF = resultMCBSENSE[resultMCBSENSE.duplicated(
        ['ISIN', 'mcCode'])]
    resultMCBSENSE.drop_duplicates(subset="ISIN", keep="first", inplace=True)
    resultMCBSENSE = resultMCBSENSE.rename(
        columns={'bseCode': 'scrip_cd', 'Security Id': 'scripname', 'Security Name': 'name'})
    resultMCBSENSE.to_json('mcbseNseAllCapScript.json', orient='records')
    # edit = EPC = MAHEPC


def getBSENSEComp():
    # nse BhavcopyCSV csv
    nseBhavdf = pd.read_csv("cm11JUN2021bhav.csv")

    # nse market-capitalisation excel
    nseMakCapdf = pd.read_excel("MCAP31032021_0.xlsx")
    # print(nseMakCapdf.columns)
    nseMakCapdf.drop(['Sr. No.'], axis=1, inplace=True)
    nseMakCapdf = nseMakCapdf.rename(
        columns={'Symbol': 'SYMBOL', 'Market capitalization \n(Rs in Lakhs)': 'McapLac'})

    resultNSE = pd.merge(nseBhavdf, nseMakCapdf, how='inner', on='SYMBOL')

    # bse List_Scrip
    bsedf = pd.read_csv("Select.csv")
    bsedf = bsedf.rename(columns={'ISIN No': 'ISIN'})
    resultBSENSE = pd.merge(resultNSE, bsedf, how='inner', on='ISIN')
    resultBSENSE.drop(['SERIES', 'TIMESTAMP', 'Unnamed: 13',
                       'Issuer Name', 'Status'], axis=1, inplace=True)  # , 'Instrument'

    resultBSENSE.to_json('resultBSENSE.json', orient='records')
    return resultBSENSE

resultBSENSE = getBSENSEComp()

def getMcBseNseAllCapScriptUR():
    # hit in brower and save json file
    # url =  'https://api.bseindia.com/BseIndiaAPI/api/GetMktData/w?ordcol=TT&strType=index&strfilter=S%26P+BSE+AllCap'
    bseAllCap = pd.DataFrame(json.load(open('BseAllCap.json'))["Table"])
    # print(bseAllCap.columns)
    bseAllCap = bseAllCap[['scrip_cd', 'URL']]
    bseAllCap = bseAllCap.rename(columns={'URL': 'url'})
    mcbseNseAllCapScript = pd.DataFrame(
        json.load(open('mcbseNseAllCapScript.json')))

    result = pd.merge(mcbseNseAllCapScript, bseAllCap,
                      how='left', on='scrip_cd')
    result.to_json('mcbseNseAllCapScriptURL.json', orient='records')
    return result


def getBSEFiter():
    bsedf = pd.read_csv("Select.csv")
    bsedf.drop(['Issuer Name'], axis=1, inplace=True)
    bsedfFilter = bsedf.loc[bsedf['Status'] == 'Active']
    bsedfFilter = bsedfFilter.loc[bsedfFilter['Instrument'] == 'Equity']


def getBSE500CompCkt():
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36", }
    url = 'https://api.bseindia.com/BseIndiaAPI/api/GetStkCurrMain/w?flag=Equity&ddlVal1=Index&ddlVal2=S%26P%20BSE%20500&m=0&pgN='
    PVList = []
    for x in range(1, 18):
        datajson = requests.get((url + str(x)), headers=headers).json()
        for row in range(len(datajson)):
            PVList.append([datajson[row]['Symbol'], datajson[row]['ScripName'],
                           datajson[row]['LongName'], datajson[row]['URL']])
    # "ATP", "Open", "High", "Low", "PreCloseRate", "PercentChange", "upperCircuit", "lowerCircuit", "Wk52High", "W2AvgQ" , "Wk52low", "MCapFF", "MCapFull"

    bsedf = pd.DataFrame(
        PVList, columns=['scrip_cd', 'scripname', 'name', 'url'])
    bsedf.to_json('bse500.json', orient='records')


# def mergeFailedMCBSENSEComp():
#     # mcdf = getMCComp()
#     resultBSENSE = getBSENSEComp()

#     mcdf = pd.DataFrame(json.load(open('mcbseAll.json')))
#     mcdf['lcn'] = mcdf['mcName'].str.lower()
#     mcdf['lsn'] = mcdf['mcName'].str.lower()

#     resultBSENSE = pd.DataFrame(json.load(open('resultBSENSE.json')))
#     # print(resultBSENSE.columns)
#     index_names = resultBSENSE[resultBSENSE['Instrument'] != 'Equity'].index
#     resultBSENSE.drop(index_names, inplace=True)
#     resultBSENSE['Face Value'] = resultBSENSE['Face Value'].astype(float)

#     # resultBSENSE['lcn'] = resultBSENSE['Company Name'].str.lower()
#     # resultBSENSE['lcn'] = resultBSENSE['lcn'].str.replace(" limited", "")
#     # resultBSENSE['lcn'] = resultBSENSE['lcn'].str.replace(" ltd.", "")
#     # resultBSENSE['lcn'] = resultBSENSE['lcn'].str.replace("'", "")
#     # resultBSENSE['lcn'] = resultBSENSE['lcn'].str.replace("-", "")
#     # resultBSENSE['lcn'] = resultBSENSE['lcn'].str.replace(" (india)", "")
#     # resultBSENSE['lcn'] = resultBSENSE['lcn'].str.replace(" (i)", "")

#     resultBSENSE['lsn'] = resultBSENSE['Security Name'].str.lower()
#     resultBSENSE['lsn'] = resultBSENSE['lsn'].str.replace("$", "")
#     resultBSENSE['lsn'] = resultBSENSE['lsn'].str.replace("-", "")
#     resultBSENSE['lsn'] = resultBSENSE['lsn'].str.replace("#39;", "")
#     resultBSENSE['lsn'] = resultBSENSE['lsn'].str.replace(" ltd.", "")
#     resultBSENSE['lsn'] = resultBSENSE['lsn'].str.replace(" ltd", "")
#     resultBSENSE['lsn'] = resultBSENSE['lsn'].str.replace(" limited", "")
#     resultBSENSE['lsn'] = resultBSENSE['lsn'].str.replace(" (india)", "")
#     resultBSENSE['lsn'] = resultBSENSE['lsn'].str.replace(" (i)", "")

#     # resultBSENSE['lsnBool'] = resultBSENSE['lsn'] == resultBSENSE['lcn']

#     # resultlcn = pd.merge(mcdf, resultBSENSE, how ='inner', on ='lcn')
#     resultlsn = pd.merge(mcdf, resultBSENSE, how='inner', on='lsn')

#     # resultNew = pd.merge(resultlsn, resultlcn, how ='inner', on ='mcName')
