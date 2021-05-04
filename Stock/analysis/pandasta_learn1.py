# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 16:20:29 2021

@author: Pritam


https://github.com/bukosabino/ta

https://pypi.org/project/ta/

pip install ta

https://technical-analysis-library-in-python.readthedocs.io/en/latest/

https://towardsdatascience.com/trading-strategy-technical-analysis-with-python-ta-lib-3ce9d6ce5614

https://towardsdatascience.com/technical-analysis-library-to-financial-datasets-with-pandas-python-4b2b390d3543

http://theautomatic.net/2021/02/02/technical-analysis-with-python/

https://www.moneycontrol.com/technical-analysis/tataconsultancyservices/TCS/monthly

https://github.com/pritamkhose/stock-python/blob/main/techCalcRoutes.py

https://www.w3schools.com/python/matplotlib_subplots.asp

https://corporatefinanceinstitute.com/resources/knowledge/trading-investing/fast-stochastic-indicator/
"""
from datetime import datetime
import os
import math
import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt 

from ta import add_all_ta_features
from ta.utils import dropna

from ta.volatility import BollingerBands, AverageTrueRange, KeltnerChannel, DonchianChannel
from ta.momentum import RSIIndicator, StochRSIIndicator, WilliamsRIndicator, ROCIndicator, StochasticOscillator, AwesomeOscillatorIndicator
from ta.trend import macd, MACD, CCIIndicator, ADXIndicator, IchimokuIndicator, WMAIndicator, SMAIndicator, EMAIndicator
from ta.volume import MFIIndicator, VolumeWeightedAveragePrice
from ta.others import DailyReturnIndicator, CumulativeReturnIndicator

fname = 'TCS'

df = pd.DataFrame(json.load(open('data/D/'+ fname +'.json')))
df['date'] = df['timestamp'].astype(str)
df['date'] = df['date'].str[0:10]
df['date'] = df['date'].apply(lambda x: datetime.fromtimestamp(int(x)))

# Clean NaN values
df = dropna(df)
# Add ta features filling NaN values
# df = add_all_ta_features(
#     df, open="open", high="high", low="low", close="close", volume="volume", fillna=True)

# momentum
indicator = RSIIndicator(close = df.close, window = 14)
df["rsi"] = indicator.rsi()

indicator = StochRSIIndicator(close=df["close"], window = 20)
df['stochrsi'] = indicator.stochrsi()
df['stochrsi_d'] = indicator.stochrsi_d()
df['stochrsi_k'] = indicator.stochrsi_k()

# FSTO
indicator = StochasticOscillator(close=df["close"], high=df["high"], low=df["low"], window = 14)
df['stoch_k'] = indicator.stoch()
df['stoch_d'] = indicator.stoch_signal()
df['stoch_fsto'] = df['stoch_d'].rolling(window=3).mean()

df["ao"] = AwesomeOscillatorIndicator(high=df["high"], low=df["low"]).awesome_oscillator()

indicator = WilliamsRIndicator(close=df["close"], high=df["high"], low=df["low"], lbp = 14)
df["williams_r"] = indicator.williams_r()

indicator = ROCIndicator(close=df["close"], window=20)
df["roc"] = indicator.roc()



# trend

# df["macd"] = macd(df.close, window_slow = 26, window_fast = 12)
indicator = MACD(close=df["close"], window_slow = 26, window_fast = 12, window_sign = 9)
df['macd'] = indicator.macd()
df['macd_signal'] = indicator.macd_signal()
df['macd_diff'] = indicator.macd_diff()

indicator = ADXIndicator(close=df["close"], high=df["high"], low=df["low"],  window=20)
df["adx"] = indicator.adx()

indicator = CCIIndicator(close=df["close"], high=df["high"], low=df["low"],  window=20)
df["cci"] = indicator.cci()

df["wma20"] =   WMAIndicator(close=df["close"], window=20).wma()

# df["ema20"] =   EMAIndicator(close=df["close"], window=20).ema_indicator()
df['EMA5'] = df['close'].ewm(span=5, adjust=False).mean()
df['EMA20'] = df['close'].ewm(span=20, adjust=False).mean()
df['EMA50'] = df['close'].ewm(span=50, adjust=False).mean()
df['EMA200'] = df['close'].ewm(span=200, adjust=False).mean()

# df["sma20"] =   SMAIndicator(close=df["close"], window=20).sma_indicator()
# df['SMA5'] = df['close'].rolling(window=5).mean()
df['SMA20'] = df['close'].rolling(window=20).mean()
# df['SMA50'] = df['close'].rolling(window=50).mean()
# df['SMA200'] = df['close'].rolling(window=200).mean()

df['MA_CO_5_20'] = df['EMA5'] > df['EMA20']
df['MA_CO_5_20'] = df['MA_CO_5_20'].replace(to_replace=True, value =1)
df['MA_CO_5_20'] = df['MA_CO_5_20'].replace(to_replace=0, value =-1)

df['MA_CO_20_50'] = df['EMA20'] > df['EMA50']
df['MA_CO_20_50'] = df['MA_CO_20_50'].replace(to_replace=True, value =1)
df['MA_CO_20_50'] = df['MA_CO_20_50'].replace(to_replace=0, value =-1)

df['MA_CO_50_200'] = df['EMA50'] > df['EMA200']
df['MA_CO_50_200'] = df['MA_CO_50_200'].replace(to_replace=True, value =1)
df['MA_CO_50_200'] = df['MA_CO_50_200'].replace(to_replace=0, value =-1)

indicator = IchimokuIndicator(high=df["high"], low=df["low"],  window1 = 9, window2 = 26, window3 = 52 )
df['ich_a'] = indicator.ichimoku_a()
df['ich_b'] = indicator.ichimoku_b()
df['ich_conv'] = indicator.ichimoku_conversion_line()
df['ich_base'] = indicator.ichimoku_base_line()

# Volume

indicator = MFIIndicator(close=df["close"], high=df["high"], low=df["low"], volume=df["volume"],  window=14)
df["mfi"] = indicator.money_flow_index()

indicator = VolumeWeightedAveragePrice(close=df["close"], high=df["high"], low=df["low"], volume=df["volume"],  window=14)
df["vwap"] = indicator.volume_weighted_average_price()


# volatility

# Bollinger Bands Indicator
indicator = BollingerBands(close=df["close"], window=20, window_dev=2)
df['bb_avg'] = indicator.bollinger_mavg()
df['bb_hb'] = indicator.bollinger_hband()
df['bb_lb'] = indicator.bollinger_lband()
# # Add Bollinger Band high/low indicator
# df['bb_bbhi'] = indicator.bollinger_hband_indicator()
# df['bb_bbli'] = indicator.bollinger_lband_indicator()

indicator = AverageTrueRange(close=df["close"], high=df["high"], low=df["low"], window=14)
df["atr"] = indicator.average_true_range()

indicator = KeltnerChannel(close=df["close"], high=df["high"], low=df["low"], window=20)
df["kc_hb"] = indicator.keltner_channel_hband()
df["kc_lb"] = indicator.keltner_channel_lband()

indicator = DonchianChannel(close=df["close"], high=df["high"], low=df["low"], window=20)
df["dc_hb"] = indicator.donchian_channel_hband()
df["dc_lb"] = indicator.donchian_channel_lband()

# daily other
df["DR"] = DailyReturnIndicator(close=df["close"]).daily_return()
df["CR"] =  CumulativeReturnIndicator(close=df["close"]).cumulative_return()

# print(df.columns)

def RSI_MFI_Action(r):
    if(r >= 80):
        action = -2 #'Overbought'
    elif(r < 80 and r > 60):
        action = -1 #'Bullish'
    elif(r < 40 and r > 20):
        action = 1 #'Bearish'
    elif(r <= 20):
        action = 2 #'Oversold'
    else:
        action = 0 #'Neutral'
    return action


def stochrsiAction(r):
    if(r >= 0.08):
        action = -1 #'high'
    elif(r <= 0.02):
        action = 1 #'low'
    else:
        action = 0 #'Neutral'
    return action

def stochAction(r):
    if(r >= 80):
        action = -1 #'high'
    elif(r <= 20):
        action = 1 #'low'
    else:
        action = 0 #'Neutral'
    return action

def williamsRAction(r):
    if(r >= -20):
        action = -1 #'high'
    elif(r <= -80):
        action = 1 #'low'
    else:
        action = 0 #'Neutral'
    return action

def rocAction(r):
    if(r >= 5):
        action = 1 #'high'
    elif(r <= -5):
        action = -1 #'low'
    else:
        action = 0 #'Neutral'
    return action

def maAction(low, med, high):
    action = 0
    return action

def aoAction(r):
    if(r >= 0):
        action = 1 #'high'
    else:
        action = -1 #'Neutral'
    return action 

# Decide Buy/ Sell
dfDecide = df[['date', 'close', 'volume' ]]

# dfDecide["rsi"] = df["rsi"].apply(lambda x: RSI_MFI_Action(x))
# dfDecide["stochrsi"] = df["stochrsi"].apply(lambda x: stochrsiAction(x))
dfDecide["stoch_d"] = df["stoch_d"].apply(lambda x: stochAction(x))
dfDecide["fsto"] = df["stoch_fsto"].apply(lambda x: stochAction(x))
dfDecide["ao"] = df["ao"].apply(lambda x: aoAction(x))

# dfDecide["williams_r"] = df["williams_r"].apply(lambda x: williamsRAction(x))
# dfDecide["roc"] = df["roc"].apply(lambda x: rocAction(x))
# dfDecide["macd"] = df["macd"] > df["macd_signal"]

# dfDecide["adx"] = df["adx"] # strenth # https://www.investopedia.com/articles/trading/07/adx-trend-indicator.asp
# dfDecide["cci"] = df["cci"].apply(lambda x: (x)) # https://www.investopedia.com/articles/active-trading/031914/how-traders-can-utilize-cci-commodity-channel-index-trade-stock-trends.asp

# dfDecide["mfi"] = df["mfi"].apply(lambda x: RSI_MFI_Action(x)) # https://www.investopedia.com/terms/m/mfi.asp
# dfDecide["vwamp"] = df["vwamp"] > df["close"]
# dfDecide["ma"] = df.MA_CO_5_20 + df.MA_CO_20_50 + df.MA_CO_50_200

# Plot graph

dflen= len(dfDecide)
df = df[dflen-200:dflen]
dfDecide= dfDecide[dflen-200:dflen]

plt.subplot(3, 1, 1)
plt.grid()
plt.plot(dfDecide.date, dfDecide.close, linewidth = '1', color='blue')

# Ichimoku plt.title("Ichimoku Cloud")
# plt.plot(df.date, df.ich_a, linewidth = '1', color='magenta', linestyle='dashed')
# plt.plot(df.date, df.ich_b, linewidth = '1', color='cyan', linestyle='dashed')
# plt.plot(df.date, df.ich_conv, linewidth = '1', color='orange')
# plt.plot(df.date, df.ich_base, linewidth = '1', color='red')

# plt.title("Bollinge Band")
# plt.plot(df.date, df.bb_avg, linewidth = '1', color='cyan', linestyle='dashed')
# plt.plot(df.date, df.bb_hb, linewidth = '1', color='green')
# plt.plot(df.date, df.bb_lb, linewidth = '1', color='red')

# plt.title("Keltner Channel")
# plt.plot(df.date, df.kc_hb, linewidth = '1', color='green')
# plt.plot(df.date, df.kc_lb, linewidth = '1', color='red')
# plt.plot(df.date, (df.kc_hb + df.kc_lb)/2, linewidth = '1', color='cyan', linestyle='dashed')

# plt.title("Donchian Channel")
# plt.plot(df.date, df.dc_hb, linewidth = '1', color='green')
# plt.plot(df.date, df.dc_lb, linewidth = '1', color='red')
# plt.plot(df.date, (df.dc_hb + df.dc_lb)/2, linewidth = '1', color='cyan', linestyle='dashed')

# plt.title("SMA")
# plt.plot(df.date, df.EMA5, linewidth = '1', color='cyan',)
# plt.plot(df.date, df.EMA20, linewidth = '1', color='green')
# plt.plot(df.date, df.EMA50, linewidth = '1', color='orange')
# plt.plot(df.date, df.EMA200, linewidth = '1', color='red')

plt.subplot(3, 1, 2)
plt.grid()
# plt.plot(df.date, df.rsi, linewidth = '1')


# plt.plot(df.date, df.stochrsi  *100, linewidth = '1')
# plt.plot(df.date, df.DR, linewidth = '1', color='green')
# plt.plot(df.date, df.CR, linewidth = '1', color='red')

# plt.plot(df.date, df.williams_r, linewidth = '1')
# plt.plot(df.date, df.roc, linewidth = '1')
# plt.plot(df.date, df.macd, linewidth = '1')
# plt.plot(df.date, df.macd_signal, linewidth = '1')

# plt.plot(df.date, df.adx, linewidth = '1')
# plt.plot(df.date, df.cci, linewidth = '1')

# plt.plot(df.date, df.atr, linewidth = '1')
# plt.plot(df.date, df.mfi, linewidth = '1')
# plt.plot(df.date, df.vwap, linewidth = '1', color='cyan')

# plt.title("Daily Cumulative Return")
# plt.plot(df.date, df.DR, linewidth = '1', color='green')
# plt.plot(df.date, df.CR, linewidth = '1', color='red')

plt.plot(df.date, df.stoch_k, linewidth = '1', color='blue',)
plt.plot(df.date, df.stoch_d, linewidth = '1', color='red')
plt.plot(df.date, df.stoch_fsto, linewidth = '1', color='green')
plt.plot(df.date, df.ao, linewidth = '1', color='magenta')

# plt.plot(df.date, df.MA_CO_5_20, linewidth = '1', color='cyan',)
# plt.plot(df.date, df.MA_CO_20_50, linewidth = '1', color='green')
# plt.plot(df.date, df.MA_CO_50_200, linewidth = '1', color='magenta')

plt.subplot(3, 1, 3)
plt.grid()
# plt.plot(dfDecide.date, dfDecide.rsi, linewidth = '1')
# plt.plot(dfDecide.date, dfDecide.stochrsi, linewidth = '1')
plt.plot(dfDecide.date, dfDecide.stoch_d, linewidth = '1')
plt.plot(dfDecide.date, dfDecide.fsto, linewidth = '1')
plt.plot(dfDecide.date, dfDecide.ao, linewidth = '1')

# plt.plot(dfDecide.date, dfDecide.williams_r, linewidth = '1')
# plt.plot(dfDecide.date, dfDecide.roc, linewidth = '1')
# plt.plot(dfDecide.date, dfDecide.macd, linewidth = '1')

# plt.plot(dfDecide.date, dfDecide.mfi, linewidth = '1')
# plt.plot(dfDecide.date, dfDecide.vwap, linewidth = '1')

# plt.plot(df.date, dfDecide.ma, linewidth = '1', color='green')

plt.gcf().autofmt_xdate()
# plt.savefig('1.svg')
plt.savefig('1.png', dpi=1600)
plt.show()