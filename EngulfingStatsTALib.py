# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 22:11:23 2021

@author: minta
"""
MT5RawDataPath = "D:\\Statistics\\MT5\\"
CandlePatternDataPath = "D:\\Statistics\\CandlePatterns\\"



import talib as ta

from datetime import datetime
#import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import MetaTrader5 as mt5


data = pd.read_csv(CandlePatternDataPath+'EURUSD_D1.csv', index_col=0, parse_dates=True)

