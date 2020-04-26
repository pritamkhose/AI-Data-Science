# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 20:43:59 2020

@author: Pritam

https://saralgyaan.com/posts/python-candlestick-chart-matplotlib-tutorial-chapter-11/
https://github.com/matplotlib/mplfinance

https://plotly.com/python/static-image-export/

https://en.wikipedia.org/wiki/Candlestick_pattern
https://www.investopedia.com/trading/candlestick-charting-what-is-it/
https://www.ig.com/en/trading-strategies/16-candlestick-patterns-every-trader-should-know-180615
https://www.adigitalblogger.com/online-share-trading/candlestick-patterns/
https://zerodha.com/varsity/chapter/getting-started-candlesticks/

http://www.niftyfuture.com/2010/11/candlestick-formula-for-doji.html
https://candlestickforum.com/pcf-personal-criteria-formulas-for-telechart-software/

https://www.investopedia.com/trading/heikin-ashi-better-candlestick/
"""

#Import the libraries
import math
import pandas_datareader as web
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import mplfinance as mpf
import IPython.display as IPydisplay

plt.style.use('fivethirtyeight')

#MarketMood = [[-1, 'Bearish'],[0, 'Neutral'],[1, 'Bullish']]
CandlePatterns = [['Big Body', 0], ['Body', 0], ['Doji', 0], ['Long Legged Doji', 0], 
                  ['Dragonfly Doji', 1], ['Gravestone Doji', -1], ['Hammer', 1],
                  ['Inverted Hammer', -1], ['Hanging Man', -1], ['Shooting Star', -1],
                  ['Long Upper Shadow', 0], ['Long Lower Shadow', 0], ['Marubozu', 0],
                  ['Spinning Top', 0], ['Shaven Head', 0], ['Shaven Bottom', 0],
                  ]
#Get the stock quote
df = web.DataReader('INFY.NS', data_source='yahoo', start='2019-01-01', end='2020-01-01')


def candlepattern(mood, moodtxt, ocdiff, Close, Open, High, Low):
  diffHL =  High - Low
  perOL= (Open - Low)/diffHL
  perCL= (Close - Low)/diffHL
  diffOHLper = perOL - perCL
  diffOC = abs(Open - Close)
  percent = [0, perOL, perCL, 1, diffOHLper]
  
  ctype = ''
  if(diffOHLper == 1):
      ctype =  'Marubozu'
  elif(diffOHLper > 0.8):
      ctype =  'Big Body'
#  elif(0.8 > diffOHLper < 0.6 ):
#      ctype =  'Big'
  elif(0.3 < diffOHLper < 0.55 and High == Close): 
      ctype =  'Shaven Head' 
  elif(0.3 < diffOHLper < 0.55 and Low == Close):
      ctype =  'Shaven Bottom' 
  elif(diffOHLper < 0.25 and High == Close ): 
      ctype =  'Hanging Man' 
  elif(diffOHLper < 0.25  and Low == Close ):
      ctype =  'Shooting Star'        
  elif(diffOHLper < 0.05):
      if(diffOC/diffHL > 2.5):
          ctype =  'Long Legged Doji'
      elif(((High - Close)/diffHL) < 0.05):
          ctype =  'Dragonfly Doji'
      elif(((Close - Low)/diffHL) < 0.05):
          ctype =  'Gravestone Doji'
      else:
          ctype =  'Doji'
#  elif(diffOHLper > 0.6 and diffOHLper < 0.4 ):
#      ctype =  'Big'
#  elif(diffOHLper < 0.2 ):
#      ctype =  'Low'
  else:
      ctype = ''
     
  return ctype #moodtxt + ' '+ ctype #[moodtxt + ' '+ ctype, percent]

# calculate
PVList=[]
for row in range(len(df)):
    moodtxt = ''
    ocdiff = df['Close'][row] - df['Open'][row] 
    if(ocdiff == 0):
        mood = 0
    elif(ocdiff > 0):
        mood = 1
        moodtxt = 'Bullish'
    else:
        mood = -1
        moodtxt = 'Bearish'
    cpattern = candlepattern(mood, moodtxt, ocdiff, df['Close'][row], df['Open'][row], df['High'][row] , df['Low'][row])    
    PV = [df.index[row], mood, ocdiff, cpattern]
    PVList.append(PV)    
df1 = pd.DataFrame(PVList, columns =['timedate', 'mood', 'ocdiff', 'cpattern']) 

mpf.plot(df,type='candle',volume=True, savefig='1.png')
IPydisplay.Image(filename='1.png')

#dffinal = df1.join(df, on='timedate', how='inner')


#fig = go.Figure(data=[go.Candlestick(x=df1['timedate'],
#                open=df['Open'],
#                high=df['High'],
#                low=df['Low'],
#                close=df['Close'])])
#fig.show()
#fig.write_image("1.png", width=2400, height=1600)


##Visualize the data
#plt.figure(figsize=(16,8))
#plt.title('Stock')
#plt.xlabel('Date', fontsize=10)
#plt.ylabel('Price USD ($)', fontsize=10)
#plt.plot(dffinal['Close'], linewidth=1,)
#plt.plot(dffinal['sma'], linewidth=1)
#plt.legend(['Avg price', 'SMA',], loc='lower right')
##plt.show()
#plt.savefig("1.png")