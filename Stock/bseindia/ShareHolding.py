#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 15 21:21:44 2022

@author: pritamkhose

https://www.bseindia.com/stock-share-price/shp/scripcode/500209/flag/7/
https://www.bseindia.com/corporates/shpPromoterNGroup.aspx?scripcd=500209&qtrid=112.00&QtrName=December%202021
or
https://www.nseindia.com/companies-listing/corporate-filings-shareholding-pattern



pip install xmltodict
https://stackoverflow.com/questions/2148119/how-to-convert-an-xml-string-to-a-dictionary

https://www.geeksforgeeks.org/reading-and-writing-xml-files-in-python/


"""


#Import the libraries
import os
import numpy as np
import pandas as pd
import json
import requests
import xmltodict


def getData():
    url =  'https://www.bseindia.com/XBRL1/500209_972021213918_SHP.xml'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    data = requests.get(url, headers=headers).text
    # Writing to xml file
    with open('infyShareHoldingQ32022.xml', 'w') as outfile: 
        outfile.write(data)
        
# getData()

# # Read to xml file
data = open('infyShareHoldingQ32022.xml', 'r').read()
data = data.replace("ï»¿", "")
# data = data.replace("in-bse-shp:", "")
data = xmltodict.parse(data)
data = json.dump(data, open('result.json', 'w'))

# Read json file in folder    
data = json.load(open('result.json'))

data =data['xbrli:xbrl']
keylist = []
for key in data.keys():
    if 'in-bse-shp:' in key: 
        keylist.append(key)
        
result = {}
#keylistData = keylist[0:38]
keylistData = ['in-bse-shp:ScripCode', 'in-bse-shp:Symbol', 'in-bse-shp:MSEISymbol', 'in-bse-shp:ISIN', 'in-bse-shp:NameOfTheCompany', 'in-bse-shp:WhetherCompanyIsSME', 'in-bse-shp:ClassOfSecurity', 'in-bse-shp:TypeOfReport', 'in-bse-shp:DateOfReport', 'in-bse-shp:ShareholdingPatternFiledUnder', 'in-bse-shp:WhetherTheListedEntityIsPublicSectorUndertaking', 'in-bse-shp:WhetherTheListedEntityHasIssuedAnyPartlyPaidUpShares', 'in-bse-shp:WhetherTheListedEntityHasIssuedAnyPartlyPaidUpSharesForPromoterAndPromoterGroup', 'in-bse-shp:WhetherTheListedEntityHasIssuedAnyPartlyPaidUpSharesForPublicShareHolder', 'in-bse-shp:WhetherTheListedEntityHasIssuedAnyPartlyPaidUpSharesForNonPromoterNonPublic', 'in-bse-shp:WhetherTheListedEntityHasIssuedAnyConvertibleSecurities', 'in-bse-shp:WhetherTheListedEntityHasIssuedAnyConvertibleSecuritiesForPromoterAndPromoterGroup', 'in-bse-shp:WhetherTheListedEntityHasIssuedAnyConvertibleSecuritiesForPublicShareHolder', 'in-bse-shp:WhetherTheListedEntityHasIssuedAnyConvertibleSecuritiesForNonPromoterNonPublic', 'in-bse-shp:WhetherTheListedEntityHasIssuedAnyWarrants', 'in-bse-shp:WhetherTheListedEntityHasIssuedAnyWarrantsForPromoterAndPromoterGroup', 'in-bse-shp:WhetherTheListedEntityHasIssuedAnyWarrantsForPublicShareHolder', 'in-bse-shp:WhetherTheListedEntityHasIssuedAnyWarrantsForNonPromoterNonPublic', 'in-bse-shp:WhetherTheListedEntityHasAnySharesAgainstWhichDepositoryReceiptsAreIssued', 'in-bse-shp:WhetherTheListedEntityHasAnySharesAgainstWhichDepositoryReceiptsAreIssuedForPromoterAndPromoterGroup', 'in-bse-shp:WhetherTheListedEntityHasAnySharesAgainstWhichDepositoryReceiptsAreIssuedForPublicShareHolder', 'in-bse-shp:WhetherTheListedEntityHasAnySharesAgainstWhichDepositoryReceiptsAreIssuedForNonPromoterNonPublic', 'in-bse-shp:WhetherTheListedEntityHasAnySharesInLockedIn', 'in-bse-shp:WhetherTheListedEntityHasAnySharesInLockedInForPromoterAndPromoterGroup', 'in-bse-shp:WhetherTheListedEntityHasAnySharesInLockedInForPublicShareHolder', 'in-bse-shp:WhetherTheListedEntityHasAnySharesInLockedInForNonPromoterNonPublic', 'in-bse-shp:WhetherAnySharesHeldByPromotersArePledgeOrOtherwiseEncumbered', 'in-bse-shp:WhetherAnySharesHeldByPromotersArePledgeOrOtherwiseEncumberedForPromoterAndPromoterGroup', 'in-bse-shp:WhetherCompanyHasEquitySharesWithDifferentialVotingRights', 'in-bse-shp:WhetherCompanyHasEquitySharesWithDifferentialVotingRightsForPromoterAndPromoterGroup', 'in-bse-shp:WhetherCompanyHasEquitySharesWithDifferentialVotingRightsForPublicShareHolder', 'in-bse-shp:WhetherCompanyHasEquitySharesWithDifferentialVotingRightsForNonPromoterNonPublic', 'in-bse-shp:WhetherTheListedEntityHasAnySignificantBeneficialOwner']
for key in keylistData:
    result[key.replace("in-bse-shp:", "")] = data[key].get('#text')

#keylistArr = keylist[38:52]
keylistArr = ['in-bse-shp:NumberOfShareholders', 'in-bse-shp:NumberOfFullyPaidUpEquityShares', 'in-bse-shp:NumberOfShares', 'in-bse-shp:ShareholdingAsAPercentageOfTotalNumberOfShares', 'in-bse-shp:NumberOfVotingRightsHeldBySameClassOfSecurities', 'in-bse-shp:NumberOfVotingRights', 'in-bse-shp:PercentageOfTotalVotingRights', 'in-bse-shp:ShareholdingAsAPercentageAssumingFullConversionOfConvertibleSecuritiesAndWarrants', 'in-bse-shp:NumberOfEquitySharesHeldInDematerializedForm' ]
# ['in-bse-shp:NumberOfSharesUnderlyingOutstandingDepositoryReceipts', 'in-bse-shp:NameOfTheShareholder' 'in-bse-shp:TypeOfPromoterShareholding', 'in-bse-shp:CategoryOfOtherNonInstitutions', 'in-bse-shp:WhetherACategoryOrMoreThan1PercentageOfShareHolding']

# dataLen = len(data[keylistArr[0]])
for key in keylistArr:
    alist = []
    for item in range(len(data[key])):
        alist.append(data[key][item].get('#text'))
        print(key, len(data[key]))
    result[key.replace("in-bse-shp:", "")] = alist #len(data[key])



json.dump(result, open('result1.json', 'w'), indent=2, sort_keys=False)
resultdata = json.load(open('result1.json'))


