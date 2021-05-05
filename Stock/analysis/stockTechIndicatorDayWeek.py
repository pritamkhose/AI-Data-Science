# -*- coding: utf-8 -*-
"""
Created on Tue May  4 22:32:39 2021

@author: Pritam

# https://www.investopedia.com/articles/trading/07/adx-trend-indicator.asp
# https://www.investopedia.com/articles/active-trading/031914/how-traders-can-utilize-cci-commodity-channel-index-trade-stock-trends.asp
# https://www.investopedia.com/terms/m/mfi.asp

"""

from datetime import datetime
import os
import numpy as np
import pandas as pd
import json

from ta.volatility import BollingerBands, AverageTrueRange, KeltnerChannel
from ta.momentum import RSIIndicator, StochRSIIndicator, WilliamsRIndicator, ROCIndicator, StochasticOscillator, AwesomeOscillatorIndicator
from ta.trend import MACD, CCIIndicator, ADXIndicator, WMAIndicator
from ta.volume import MFIIndicator, VolumeWeightedAveragePrice

dirPath = 'E:/Code/python/AIDataScience/Stock/moneycontrol/data/'


def createDir():
    folderList = ['techD/', 'techW/', 'techM/']
    for x in folderList:
        try:
            if not os.path.exists(dirPath + x):
                os.makedirs(dirPath + x)
        except OSError as err:
            print(err)


def getData():
    data = []
    for path, subdirs, files in os.walk(dirPath):
        for name in files:
            if ".rar" in name:
                continue
            else:
                data.append(os.path.join(path, name))
    return data


def calcHLOCV(dftemp, sample):
    dfH = dftemp.high.resample(sample).max().to_frame()
    dfL = dftemp.low.resample(sample).min().to_frame()
    dfO = dftemp.open.resample(sample).first().to_frame()
    dfC = dftemp.close.resample(sample).last().to_frame()
    dfV = dftemp.volume.resample(sample).sum().to_frame()

    PVList = []
    for row in range(len(dfH)):
        if(dfV['volume'][row] != 0):
            PV = [dfH.index[row], dfH['high'][row], dfL['low'][row],
                  dfO['open'][row], dfC['close'][row], dfV['volume'][row]]
            PVList.append(PV)
    dftemp = pd.DataFrame(
        PVList, columns=['time', 'high', 'low', 'open', 'close', 'volume'])
    return dftemp


def processData(fileList, dirPath):
    folderList = ['5Y/', 'W/', 'M/']
    for x in folderList:
        try:
            if not os.path.exists(dirPath + x):
                os.makedirs(dirPath + x)
        except OSError as err:
            print(err)

    for fpath in fileList:
        try:
            fname = fpath.split('/')
            fname = (fname[len(fname)-1]).replace('.json', '')
            print(fname)

            df = pd.DataFrame(json.load(open(fpath))['g1'])
            df[['open', 'high', 'low', 'close', 'volume']] = df[[
                'open', 'high', 'low', 'close', 'volume']].astype(float)
            df.rename({'date': 'time'}, axis=1, inplace=True)
            df = df.drop('value', axis=1)

            # take last 5Y or min days
            dflen = len(df)
            df = df[dflen-1500:dflen]
            df.to_json(dirPath + '5Y/' + fname+'.json', orient='records')

            df['time'] = pd.to_datetime(df['time'])
            df.set_index('time', inplace=True)

            dfW = calcHLOCV(df, 'W')
            dfW['time'] = dfW['time'].astype(str)
            dfW.to_json(dirPath + str('W/' + fname+'.json'), orient='records')

            dfM = calcHLOCV(df, 'M')
            dfM['time'] = dfM['time'].astype(str)
            dfM.to_json(dirPath + str('M/' + fname+'.json'), orient='records')

        except Exception as e:
            print(fname, str(e))

    return 0


def RSI_MFI_Action(r):
    if(r >= 80):
        action = -2  # 'Overbought'
    elif(r < 80 and r > 60):
        action = -1  # 'Bullish'
    elif(r < 40 and r > 20):
        action = 1  # 'Bearish'
    elif(r <= 20):
        action = 2  # 'Oversold'
    else:
        action = 0  # 'Neutral'
    return action


def stochrsiAction(r):
    if(r >= 0.08):
        action = -1  # 'high'
    elif(r <= 0.02):
        action = 1  # 'low'
    else:
        action = 0  # 'Neutral'
    return action


def stochAction(r):
    if(r >= 80):
        action = -1  # 'high'
    elif(r <= 20):
        action = 1  # 'low'
    else:
        action = 0  # 'Neutral'
    return action


def williamsRAction(r):
    if(r >= -20):
        action = -1  # 'high'
    elif(r <= -80):
        action = 1  # 'low'
    else:
        action = 0  # 'Neutral'
    return action


def adxAction(r):
    if(r >= 75):
        action = 2  # Extremely Strong Trend
    elif(r < 75 and r > 50):
        action = 1  # Very Strong Trend
    elif(r < 50 and r > 25):
        action = 0  # Strong Trend
    # elif(r <= 25):
    #     action = -1
    else:
        action = -1  # Absent or Weak or Neutral Trend
    return action


def cciAction(r):
    if(r >= 100):
        action = 2  # Extremely Strong
    elif(r < 100 and r > 50):
        action = 1  # Strong
    elif(r < 50 and r > -50):
        action = 0
    elif(r < -50 and r > -100):  # Neutral
        action = -1  # Weak
    else:
        action = -2  # Absent
    return action


def rocAction(r):
    if(r >= 5):
        action = 1  # 'high'
    elif(r <= -5):
        action = -1  # 'low'
    else:
        action = 0  # 'Neutral'
    return action


def aoAction(r):
    if(r >= 0):
        action = 1  # 'high'
    else:
        action = -1  # 'Neutral'
    return action


def getPivot(df):
    dftemp = df[['time', 'close', 'high', 'low']]
    dftemp['close5d'] = dftemp['close'].rolling(window=5).mean()
    dftemp['high5d'] = dftemp['high'].rolling(window=5).mean()
    dftemp['low5d'] = dftemp['low'].rolling(window=5).mean()

    dftemp['hl'] = dftemp['high5d'] - dftemp['low5d']
    dftemp['P'] = (dftemp['close5d'] + dftemp['high5d'] + dftemp['low5d']) / 3

    # Classic
    dftemp['R1'] = (2 * dftemp['P']) - dftemp['low']
    dftemp['S1'] = (2 * dftemp['P']) - dftemp['high']
    dftemp['R2'] = dftemp['P'] + dftemp['hl']
    dftemp['S2'] = dftemp['P'] - dftemp['hl']
    dftemp['R3'] = dftemp['high'] + (2 * (dftemp['P'] - dftemp['low']))
    dftemp['S3'] = dftemp['low'] - (2 * (dftemp['high'] - dftemp['P']))

    # Fibonacci
    dftemp['fib_R1'] = dftemp['P'] + (0.382 * dftemp['hl'])
    dftemp['fib_S1'] = dftemp['P'] - (0.382 * dftemp['hl'])
    dftemp['fib_R2'] = dftemp['P'] + (0.618 * dftemp['hl'])
    dftemp['fib_S2'] = dftemp['P'] - (0.618 * dftemp['hl'])
    dftemp['fib_R3'] = dftemp['P'] + (1 * dftemp['hl'])
    dftemp['fib_S3'] = dftemp['P'] - (1 * dftemp['hl'])

    items = ['P', 'S1', 'R1', 'S2', 'R2', 'S3', 'R3', 'fib_S1',
             'fib_R1', 'fib_S2', 'fib_R2', 'fib_S3', 'fib_R3']
    for row in items:
        key = str('d_' + row)
        dftemp[key] = dftemp[row] > dftemp['close5d']
        # dftemp[key] = dftemp[row] > dftemp['close5d']
    dftemp = dftemp.replace({np.nan: None, True: 1, False: -1})
    dftemp = dftemp.drop(['close5d', 'high5d', 'low5d',
                          'hl', 'close', 'high', 'low'], axis=1)
    return dftemp


def calculateIndictor(fileList, dirPath):
    for fpath in fileList:
        try:
            fname = fpath.split('/')
            fname = (fname[len(fname)-1]).replace('.json', '')
            print(fname)
            df = pd.DataFrame(json.load(open(dirPath + '5Y/' + fname+'.json')))

            # momentum
            df["rsi"] = RSIIndicator(close=df.close, window=14).rsi()

            indicator = StochRSIIndicator(close=df["close"], window=20)
            df['stochrsi'] = indicator.stochrsi()
            df['stochrsi_d'] = indicator.stochrsi_d()
            df['stochrsi_k'] = indicator.stochrsi_k()

            # FSTO
            indicator = StochasticOscillator(
                close=df["close"], high=df["high"], low=df["low"], window=14)
            df['stoch_k'] = indicator.stoch()
            df['stoch_d'] = indicator.stoch_signal()
            df['stoch_fsto'] = df['stoch_d'].rolling(window=3).mean()

            df["ao"] = AwesomeOscillatorIndicator(
                high=df["high"], low=df["low"]).awesome_oscillator()

            df["williams_r"] = WilliamsRIndicator(
                close=df["close"], high=df["high"], low=df["low"], lbp=14).williams_r()

            df["roc"] = ROCIndicator(close=df["close"], window=20).roc()

            # trend

            # df["macd"] = macd(df.close, window_slow = 26, window_fast = 12)
            indicator = MACD(
                close=df["close"], window_slow=26, window_fast=12, window_sign=9)
            df['macd'] = indicator.macd()
            df['macd_signal'] = indicator.macd_signal()
            df['macd_diff'] = indicator.macd_diff()

            indicator = ADXIndicator(
                close=df["close"], high=df["high"], low=df["low"],  window=20)
            df["adx"] = indicator.adx()

            indicator = CCIIndicator(
                close=df["close"], high=df["high"], low=df["low"],  window=20)
            df["cci"] = indicator.cci()

            df["wma20"] = WMAIndicator(close=df["close"], window=20).wma()

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
            df['MA_CO_5_20'] = df['MA_CO_5_20'].replace(
                to_replace=True, value=1)
            df['MA_CO_5_20'] = df['MA_CO_5_20'].replace(to_replace=0, value=-1)

            df['MA_CO_20_50'] = df['EMA20'] > df['EMA50']
            df['MA_CO_20_50'] = df['MA_CO_20_50'].replace(
                to_replace=True, value=1)
            df['MA_CO_20_50'] = df['MA_CO_20_50'].replace(
                to_replace=0, value=-1)

            df['MA_CO_50_200'] = df['EMA50'] > df['EMA200']
            df['MA_CO_50_200'] = df['MA_CO_50_200'].replace(
                to_replace=True, value=1)
            df['MA_CO_50_200'] = df['MA_CO_50_200'].replace(
                to_replace=0, value=-1)

            # Volume
            df['SMAv20'] = df['volume'].rolling(window=20).mean()
            df['SMAv20'] = df['SMAv20'] / df['volume']
            df['EMAv20'] = df['volume'].ewm(span=20, adjust=False).mean()
            df['EMAv20'] = df['EMAv20'] / df['volume']

            df["mfi"] = MFIIndicator(close=df["close"], high=df["high"],
                                     low=df["low"], volume=df["volume"],  window=14).money_flow_index()

            df["vwamp"] = VolumeWeightedAveragePrice(
                close=df["close"], high=df["high"], low=df["low"], volume=df["volume"],  window=14).volume_weighted_average_price()

            # volatility
            indicator = BollingerBands(
                close=df["close"], window=20, window_dev=2)
            df['bb_avg'] = indicator.bollinger_mavg()
            df['bb_hb'] = indicator.bollinger_hband()
            df['bb_lb'] = indicator.bollinger_lband()

            df["atr"] = AverageTrueRange(
                close=df["close"], high=df["high"], low=df["low"], window=14).average_true_range()

            indicator = KeltnerChannel(
                close=df["close"], high=df["high"], low=df["low"], window=20)
            df["kc_hb"] = indicator.keltner_channel_hband()
            df["kc_lb"] = indicator.keltner_channel_lband()

            # Decsion

            df["d_rsi"] = df["rsi"].apply(lambda x: RSI_MFI_Action(x))
            df["d_stochrsi"] = df["stochrsi"].apply(
                lambda x: stochrsiAction(x))
            df["d_stoch_d"] = df["stoch_d"].apply(lambda x: stochAction(x))
            df["d_fsto"] = df["stoch_fsto"].apply(lambda x: stochAction(x))
            df["d_ao"] = df["ao"].apply(lambda x: aoAction(x))

            df["d_williams_r"] = df["williams_r"].apply(
                lambda x: williamsRAction(x))
            df["d_roc"] = df["roc"].apply(lambda x: rocAction(x))
            df["d_macd"] = df["macd"] > df["macd_signal"]
            df['d_macd'] = df['d_macd'].map({True: 1, False: -1})

            df["d_adx"] = df["adx"].apply(lambda x: adxAction(x))
            df["d_cci"] = df["cci"].apply(lambda x: cciAction(x))

            df["d_mfi"] = df["mfi"].apply(lambda x: RSI_MFI_Action(x))
            df["d_vwamp"] = df["vwamp"] > df["close"]
            df["d_vwamp"] = df['d_vwamp'].map({True: 1, False: -1})
            df["d_ma"] = df.MA_CO_5_20 + df.MA_CO_20_50 + df.MA_CO_50_200

            # Pivot
            df = pd.merge(df, getPivot(df), how='inner', on='time')

            tempColumns = ['rsi', 'stochrsi', 'stochrsi_d', 'stochrsi_k', 'stoch_k', 'stoch_d', 'stoch_fsto', 'ao',
                           'williams_r', 'roc', 'macd', 'macd_signal', 'macd_diff', 'adx', 'cci', 'wma20', 'EMA5', 'EMA20',
                           'EMA50', 'EMA200', 'SMA20', 'SMAv20', 'EMAv20', 'mfi', 'vwamp', 'bb_avg', 'bb_hb', 'bb_lb',
                           'atr', 'kc_hb', 'kc_lb', 'P', 'R1', 'S1', 'R2', 'S2', 'R3', 'S3',
                           'fib_R1', 'fib_S1', 'fib_R2', 'fib_S2', 'fib_R3', 'fib_S3']
            for dfname in tempColumns:
                df[dfname] = df[dfname].round(2)

            df.to_json(dirPath + str('techD/' + fname+'.json'),
                       orient='records')

        except Exception as e:
            print(fname, str(e))

        # return df


createDir()
fileList = getData()
# processData(fileList, dirPath)

df = calculateIndictor(fileList, dirPath)  # fileList[0:1]
# print(df.columns)
