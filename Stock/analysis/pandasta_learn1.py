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
"""
import os
import math
import numpy as np
import pandas as pd
import json

from ta import add_all_ta_features
from ta.utils import dropna

from ta.volatility import BollingerBands, AverageTrueRange, KeltnerChannel, DonchianChannel
from ta.momentum import RSIIndicator, StochRSIIndicator, WilliamsRIndicator, ROCIndicator
from ta.trend import macd, MACD, CCIIndicator, ADXIndicator, IchimokuIndicator, WMAIndicator, SMAIndicator, EMAIndicator
from ta.volume import MFIIndicator, VolumeWeightedAveragePrice
from ta.others import DailyReturnIndicator, CumulativeReturnIndicator

fname = 'TCS'

df = pd.DataFrame(json.load(open('data/D/'+ fname +'.json')))

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
df['stochrsi_d'] = indicator.stochrsi_k()

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
df["ema20"] =   EMAIndicator(close=df["close"], window=20).ema_indicator()
df["sma20"] =   SMAIndicator(close=df["close"], window=20).sma_indicator()


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

print(df.columns)