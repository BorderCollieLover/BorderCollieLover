# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 17:48:43 2021

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


def RetrieveMT5Data(ticker, timeframe):
    # connect to MetaTrader 5
    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()
        return(None)
    
    #this is the peculiarity of the copy_rates, use datetime.now() to ensure retrieval of full history 
    #Use a large buffer which is usually enough for H and D bars 
    #Also in MT5, in Tools --> Options --> Charts, set "Max bars in charts" to "Unlimited"  (not sure if it is necessary but it works)
    data = mt5.copy_rates_from(ticker, getattr(mt5, "TIMEFRAME_"+timeframe), datetime.now(), 5000000)
    
    if (data.size == 0):
        print("No data is retrieved.")
        mt5.shutdown()
        return (None)
    
    
    data_time = [datetime.utcfromtimestamp(x[0]).strftime('%Y-%m-%d %H:%M:%S')  for x in data]
    data_timestamp = [x[0] for x in data]
    data_o = [x[1] for x in data]
    data_h = [x[2] for x in data]
    data_l = [x[3] for x in data]
    data_c = [x[4] for x in data]
    data_tickv = [x[5] for x in data]
    data_spread = [x[6] for x in data]
    data_v = [x[7] for x in data]
    
    output = pd.DataFrame(
        {'o': data_o,
         'h': data_h, 
         'l': data_l, 
         'c': data_c, 
         'timestamp': data_timestamp, 
         'tick_v': data_tickv, 
         'spread': data_spread, 
         'volume': data_v
        }
        )
    output.index = data_time
    
    #data_time2 = datetime.utcfromtimestamp(data_time).strftime('%Y-%m-%d %H:%M:%S')
    
    
    #print(data_time)
    #print(ticker, ": ", len(data), " rows copied")
    #for val in data[:10]: print(val)
    
    mt5.shutdown()
    output.to_csv(MT5RawDataPath+ticker+"_"+timeframe+".csv")
    return (output)

def FindPatterns(data, ticker, timeframe):
    candle_names = ta.get_function_groups()['Pattern Recognition']
    
    for candle in candle_names:
    # below is same as;
    # df["CDL3LINESTRIKE"] = talib.CDL3LINESTRIKE(op, hi, lo, cl)
        data[candle] = getattr(ta, candle)(data.o, data.h, data.l, data.c)
    
    data.to_csv(CandlePatternDataPath +ticker+"_"+timeframe+".csv")
    return(data)
        
    
    
tickers = [ 'EURUSD',  'GBPUSD', 'USDJPY', 'USDCHF', 'USDCAD', 'AUDUSD', 'NZDUSD', 'EURGBP', 'EURJPY', 'GBPJPY', 'AUDJPY', 'AUDNZD', 'GOLD', 'SILVER', 'BTCUSD', 'ETHUSD']
periods = ['W1', 'D1', 'H1']

#data = RetrieveMT5Data("USDCNH", "D1")

for ticker in tickers: 
    for period in periods: 
        print(ticker, period)
        #data = RetrieveMT5Data(ticker, period)
        #data2 = FindPatterns(data, ticker, period)

