# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 20:43:59 2020

@author: Pritam

https://github.com/sunilgug/Candlestick_patterns

http://www.niftyfuture.com/2010/11/candlestick-formula-for-doji.html
https://candlestickforum.com/pcf-personal-criteria-formulas-for-telechart-software/

https://stackoverflow.com/questions/32400867/pandas-read-csv-from-url
"""

import pandas as pd
import numpy as np
from nsepy import get_history
import datetime
import json
import requests
import io
import os

def candle_score(lst_0,lst_1,lst_2):    
    
    O0,H0,L0,C0=lst_0[0],lst_0[1],lst_0[2],lst_0[3]
    O1,H1,L1,C1=lst_1[0],lst_1[1],lst_1[2],lst_1[3]
    O2,H2,L2,C2=lst_2[0],lst_2[1],lst_2[2],lst_2[3]
    
    DojiSize = 0.1
    
    doji=(abs(O0 - C0) <= (H0 - L0) * DojiSize)
    
    marubozu = (abs(O0 - C0) == (H0 - L0))
    
    hammer=(((H0 - L0)>3*(O0 -C0)) &  ((C0 - L0)/(.001 + H0 - L0) > 0.6) & ((O0 - L0)/(.001 + H0 - L0) > 0.6))
    
    inverted_hammer=(((H0 - L0)>3*(O0 -C0)) &  ((H0 - C0)/(.001 + H0 - L0) > 0.6) & ((H0 - O0)/(.001 + H0 - L0) > 0.6))
    
    bullish_reversal= (O2 > C2)&(O1 > C1)&doji
    
    bearish_reversal= (O2 < C2)&(O1 < C1)&doji
    
    evening_star=(C2 > O2) & (min(O1, C1) > C2) & (O0 < min(O1, C1)) & (C0 < O0 )
    
    morning_star=(C2 < O2) & (min(O1, C1) < C2) & (O0 > min(O1, C1)) & (C0 > O0 )
    
    shooting_Star_bearish=(O1 < C1) & (O0 > C1) & ((H0 - max(O0, C0)) >= abs(O0 - C0) * 3) & ((min(C0, O0) - L0 )<= abs(O0 - C0)) & inverted_hammer
    
    shooting_Star_bullish=(O1 > C1) & (O0 < C1) & ((H0 - max(O0, C0)) >= abs(O0 - C0) * 3) & ((min(C0, O0) - L0 )<= abs(O0 - C0)) & inverted_hammer
    
    bearish_harami=(C1 > O1) & (O0 > C0) & (O0 <= C1) & (O1 <= C0) & ((O0 - C0) < (C1 - O1 ))
    
    Bullish_Harami=(O1 > C1) & (C0 > O0) & (C0 <= O1) & (C1 <= O0) & ((C0 - O0) < (O1 - C1))
    
    Bearish_Engulfing=((C1 > O1) & (O0 > C0)) & ((O0 >= C1) & (O1 >= C0)) & ((O0 - C0) > (C1 - O1 ))
    
    Bullish_Engulfing=(O1 > C1) & (C0 > O0) & (C0 >= O1) & (C1 >= O0) & ((C0 - O0) > (O1 - C1 ))
    
    Piercing_Line_bullish=(C1 < O1) & (C0 > O0) & (O0 < L1) & (C0 > C1)& (C0>((O1 + C1)/2)) & (C0 < O1)

    Hanging_Man_bullish=(C1 < O1) & (O0 < L1) & (C0>((O1 + C1)/2)) & (C0 < O1) & hammer

    Hanging_Man_bearish=(C1 > O1) & (C0>((O1 + C1)/2)) & (C0 < O1) & hammer
    
#   DarkCloud = ((C1 > O1) & (((C1 + O1) / 2) > C0) & (O0 > C0) & (O0 > C1) & (C0 > O1) & ((O0 – C0) / (.001 + (H0 – L0)) > .6))
    DarkCloud = ((C1 > O1) & (((C1 + O1) / 2) > C0))
#    Hanging_Man = (((H0 – L0) > 4 * (O0 – C0)) & ((C0 – L0) / (.001 + H0 – L0) >= 0.75) & ((O0 – L0) / (0.001 + H0 – L0) >= .075)))

    strCandle=[]
    candle_score=0
    
    if doji:
        strCandle.append('doji')
    if marubozu:
        strCandle.append('marubozu')
        
        
    if evening_star:
        strCandle.append('evening_star')
        candle_score=candle_score-1
    if morning_star:
        strCandle.append('morning_star')
        candle_score=candle_score+1
    if shooting_Star_bearish:
        strCandle.append('shooting_Star_bearish')
        candle_score=candle_score-1
    if shooting_Star_bullish:
        strCandle.append('shooting_Star_bullish')
        candle_score=candle_score-1
    if    hammer:
        strCandle.append('hammer')
    if    inverted_hammer:
        strCandle.append('inverted_hammer')
    if    bearish_harami:
        strCandle.append('bearish_harami')
        candle_score=candle_score-1
    if    Bullish_Harami:
        strCandle.append('Bullish_Harami')
        candle_score=candle_score+1
    if    Bearish_Engulfing:
        strCandle.append('Bearish_Engulfing')
        candle_score=candle_score-1
    if   Bullish_Engulfing:
        strCandle.append('Bullish_Engulfing')
        candle_score=candle_score+1
    if    bullish_reversal:
        strCandle.append('bullish_reversal')
        candle_score=candle_score+1
    if    bearish_reversal:
        strCandle.append('bearish_reversal')
        candle_score=candle_score-1
    if    Piercing_Line_bullish:
        strCandle.append('Piercing_Line_bullish')
        candle_score=candle_score+1
    if    Hanging_Man_bearish:
        strCandle.append('Hanging_Man_bearish')
        candle_score=candle_score-1
    if    Hanging_Man_bullish:
        strCandle.append('Hanging_Man_bullish')
        candle_score=candle_score+1
    if    DarkCloud:
        strCandle.append('Dark_Cloud')    
        
    #return candle_score
    return candle_score,strCandle

def candle_df(df):
    #df_candle=first_letter_upper(df)
    df_candle=df.copy()
    df_candle['candle_score']=0
    df_candle['candle_pattern']=[]


    for c in range(2,len(df_candle)):
        cscore,cpattern=0,''
        lst_2=[df_candle['Open'].iloc[c-2],df_candle['High'].iloc[c-2],df_candle['Low'].iloc[c-2],df_candle['Close'].iloc[c-2]]
        lst_1=[df_candle['Open'].iloc[c-1],df_candle['High'].iloc[c-1],df_candle['Low'].iloc[c-1],df_candle['Close'].iloc[c-1]]
        lst_0=[df_candle['Open'].iloc[c],df_candle['High'].iloc[c],df_candle['Low'].iloc[c],df_candle['Close'].iloc[c]]
        cscore,cpattern=candle_score(lst_0,lst_1,lst_2)    
        df_candle['candle_score'].iat[c]=cscore
        df_candle['candle_pattern'].iat[c]=cpattern
    
    df_candle['candle_cumsum']=df_candle['candle_score'].rolling(3).sum()
    
    return df_candle


#to_dt=datetime.datetime.now().date()
#from_dt=to_dt-datetime.timedelta(days=3000)
#
#df=get_history('NIFTY',from_dt,to_dt,index=True)


#1d 5d max
compname = 'yb'
#url = 'https://www.moneycontrol.com/mc/widget/basicchart/get_chart_value?classic=true&dur=max&sc_did=' + compname
#stock = requests.get(url).json()['g1']
#PVList = [];
#for row in range(len(stock)):
#    PVList.append([pd.to_datetime(stock[row]['date']), float(stock[row]['value']), float(stock[row]['open']) , float(stock[row]['close']), float(stock[row]['low']), float(stock[row]['high']), float(stock[row]['volume'])])
#df = pd.DataFrame(PVList ,columns =['date', 'value', 'Open', 'Close', 'Low', 'High', 'Volume'])
##    PVList.append([stock[row]['date'], float(stock[row]['value']), float(stock[row]['volume'])])
##df = pd.DataFrame(PVList ,columns =['date', 'value', 'volume']) 

colnames=['Date', 'Open','High','Low','Close','Volume','NA','Final','NA2','FV'] 
url = 'https://www.moneycontrol.com/tech_charts/nse/his/'+compname+'.csv?classic=true'
stock = requests.get(url).content
df=pd.read_csv(io.StringIO(stock.decode('utf-8')), names=colnames, header=None)
PVList = [];
#for row in range(len(stock)):
#    PVList.append([pd.to_datetime(stock[row]['date']), float(stock[row]['value']), float(stock[row]['open']) , float(stock[row]['close']), float(stock[row]['low']), float(stock[row]['high']), float(stock[row]['volume'])])
#df = pd.DataFrame(PVList ,columns =['date', 'value', 'Open', 'Close', 'Low', 'High', 'Volume'])
#    PVList.append([stock[row]['date'], float(stock[row]['value']), float(stock[row]['volume'])])
#df = pd.DataFrame(PVList ,columns =['date', 'value', 'volume']) 



df1=candle_df(df)
#print(df1[:][['candle_pattern','candle_score']])

df2 = (df1[:][['Date', 'Open','High','Low','Close','Volume','candle_pattern','candle_score']])

if not os.path.exists('data'):
    os.makedirs('data')
# Writing to json file
df2.to_json('data/'+compname + '1.json', orient='records', lines=True)    
#with open('data/'+compname + '.json', 'w') as outfile: 
#    outfile.write(json.dumps(datajson))