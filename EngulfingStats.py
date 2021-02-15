# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
from datetime import datetime 
import numpy as np 

MT5_Data_PATH = r"C:\Users\minta\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Files\\"
MT5_Data_PATH = r"C:\Users\minta\AppData\Roaming\MetaQuotes\Terminal\24F345EB9F291441AFE537834F9D8A19\MQL5\Files\\"

## C:\Users\minta\AppData\Roaming\MetaQuotes\Terminal\24F345EB9F291441AFE537834F9D8A19\MQL5\Files
Statistics_PATH = r"D:\Statistics\\"
Engulfing_Data_PATH = Statistics_PATH + "Engulfing Data\\"
Engulfing_Summary_PATH = Statistics_PATH + "Engulfing Summaries\\"
Engulfing_CrossSectional_PATH = Statistics_PATH + "Engulfing CrossSectional\\"

cutoff_date = pd.to_datetime("20000101", format='%Y%m%d')
custom_date_parser = lambda x: datetime.strptime(x, "%Y%m%d:%H")

#statistics
#'As %of Total' is based on the full data set, i.e. the number 'Counts' divided by the size of the full data set 
#Every other statistic is expressed as of a percentage of Counts 
engulfing_stats_columns = ['Counts', 'Bullish Bars', 'Bullish %', 'Bearish Bars', 'Bearish %', 
                           'Bar+1 Consistent', 'Bar+1 Consistent %', 'Bar+2 Consistent', 'Bar+2 Consistent %', 
                           'Bar+1 Close Con.', 'Bar+1 Close Con. %', 'Bar+2 Close Con.', 'Bar+2 Close Cons. %',
                           'Bar+1 H/L Con.', 'Bar+1 H/L Con. %', 'Bar+2 H/L Con.', 'Bar+2 H/L Cons. %', 
                           'Bar+1 Opp. H/L' , 'Bar+1 Opp. H/L %'
                           ]
#1. Over all data set
#2. Engulfing bars that have reversal 
#3. Engulfing bars that reverse from at least two consecutive opposite bars 
#4. Engulfing bars that are of at least 1-ATR length
#5. Engulfing bars that are reversal and of at least 1-ATR length 
#6. Engulfing bars that are also outside bars 
#7. If the next bar is of the same direction 
#8. If the next bar showed continuation in close price 
#9. If the next bar showed continuation in high/low 
#10-12. Engulfing fails 
#13. If the next bar made an opposite high or low, i.e. for a bullish engulfing the following bar made a lower low for for a bearish engulfing, the following bar made a higher high
#14. If the previous bar is greater than the ATR -- this is for insider bars 
stat_names = ['FullData', 'ReversalBar', 'Reversal2', 'BarSize', 'ReversalandSize', 'EngulfingandOutside', 
              'Bar1SameColor', 'Bar1CloseCont', 'Bar1HLCont',
              'Bar1DiffColor', 'Bar1CloseFail', 'Bar1HLFail',
              'Bar1OppHL', 'PrevBarSize']
stat_names_bull = [x + "_bull" for x in stat_names] 
stat_names_bear = [x + "_bear" for x in stat_names]  

tickers = [ 'EURUSD',  'GBPUSD', 'USDJPY', 'USDCHF', 'USDCAD', 'AUDUSD', 'NZDUSD', 'EURGBP', 'EURJPY', 'GBPJPY', 'AUDJPY', 'AUDNZD', 'GOLD', 'SILVER', 'BTCUSD', 'ETHUSD']
tickers_bull = [x + "_bull" for x in tickers] 
tickers_bear = [x + "_bear" for x in tickers] 


periods = ['W1', 'D1', 'H1']
engulfing_toggles  = [True, False]        
bartypes =["", "bullbars", "bearbars"]
patterns =["Engulfing", "Outside", "Inside"]




def EngulfingStatisticsOneSlice(data):
    num_of_columns = len(engulfing_stats_columns)
    #sssssssprint(num_of_columns)
    
    SliceStats = pd.DataFrame(np.zeros((1,num_of_columns)), columns = engulfing_stats_columns)
    SliceStats.loc[0,'Counts'] = data.Close.count()
    #SliceStats.loc[0,'As % of Total'] = SliceStats.loc[0,'Counts']/total_count
    
    SliceStats.loc[0, 'Bullish Bars'] = sum(data.BullCandle)
    SliceStats.loc[0, 'Bullish %'] = SliceStats.loc[0, 'Bullish Bars']/SliceStats.loc[0,'Counts']
    
    SliceStats.loc[0, 'Bearish Bars'] = SliceStats.loc[0,'Counts'] - sum(data.BullCandle)
    SliceStats.loc[0, 'Bearish %'] = 1 - SliceStats.loc[0, 'Bullish %'] 
    
    SliceStats.loc[0, 'Bar+1 Consistent'] = sum(data.Continuation)
    SliceStats.loc[0, 'Bar+1 Consistent %'] = SliceStats.loc[0, 'Bar+1 Consistent']/ SliceStats.loc[0,'Counts']
    
    SliceStats.loc[0, 'Bar+2 Consistent'] = sum(data.Continuation2)
    SliceStats.loc[0, 'Bar+2 Consistent %'] = SliceStats.loc[0, 'Bar+2 Consistent']/ SliceStats.loc[0,'Counts']
    
    SliceStats.loc[0, 'Bar+1 Close Con.'] = sum(data.CloseContinuation)
    SliceStats.loc[0, 'Bar+1 Close Con. %'] = SliceStats.loc[0, 'Bar+1 Close Con.']/ SliceStats.loc[0,'Counts']
    
    SliceStats.loc[0, 'Bar+2 Close Con.'] = sum(data.CloseContinuation2)
    SliceStats.loc[0, 'Bar+2 Close Cons. %'] = SliceStats.loc[0, 'Bar+2 Close Con.']/ SliceStats.loc[0,'Counts']
    
    SliceStats.loc[0, 'Bar+1 H/L Con.'] = sum(data.HighLowContinuation)
    SliceStats.loc[0, 'Bar+1 H/L Con. %'] = SliceStats.loc[0, 'Bar+1 H/L Con.']/ SliceStats.loc[0,'Counts']
    
    SliceStats.loc[0, 'Bar+2 H/L Con.'] = sum(data.HighLowContinuation2)
    SliceStats.loc[0, 'Bar+2 H/L Cons. %'] = SliceStats.loc[0, 'Bar+2 H/L Con.']/ SliceStats.loc[0,'Counts']
    
    SliceStats.loc[0, 'Bar+1 Opp. H/L'] = sum(data.OppHighLow)
    SliceStats.loc[0, 'Bar+1 Opp. H/L %'] = SliceStats.loc[0, 'Bar+1 Opp. H/L']/ SliceStats.loc[0,'Counts']
    
    #print(engulfing_stats_columns)
    #print(SliceStats.columns)
    #print(SliceStats)
    return(SliceStats) # return from EngulfingStatisticsOneSlice

def EngulfingStatisticsOneDataBatch(data, pattern):
    full_data = data 
    #total_data_rows = data.Close.count()
    
    index_len  = len(stat_names)
    summary_stats = pd.DataFrame(np.zeros((index_len,len(engulfing_stats_columns) )), index=stat_names, columns = engulfing_stats_columns)
    
    #1. 
    i = 0 
    cur_stat = EngulfingStatisticsOneSlice(data)
    summary_stats.loc[stat_names[i]] = cur_stat.loc[0]
    
    #2.
    i = i + 1 
    data = full_data.loc[full_data.ReverseAfter>0]
    cur_stat = EngulfingStatisticsOneSlice(data)
    summary_stats.loc[stat_names[i]] = cur_stat.loc[0]
    
    #3.
    i = i+1
    data = full_data.loc[full_data.ReverseAfter>1]
    cur_stat = EngulfingStatisticsOneSlice(data)
    summary_stats.loc[stat_names[i]] = cur_stat.loc[0]
    
    #4. 
    i = i+1
    data = full_data.loc[full_data.SmallBar == False]
    cur_stat = EngulfingStatisticsOneSlice(data)
    summary_stats.loc[stat_names[i]] = cur_stat.loc[0]
    
    #5. 
    i = i+1
    data = full_data.loc[(full_data.SmallBar == False) & (full_data.ReverseAfter>0)]
    cur_stat = EngulfingStatisticsOneSlice(data)
    summary_stats.loc[stat_names[i]] = cur_stat.loc[0]
    
    #6. 
    i = i+1
    if (pattern == "Engulfing"): 
        data = full_data.loc[full_data.Outside]
    elif (pattern =="Outside"):
        data = full_data.loc[full_data.Engulfing]
    else: 
        data = full_data.loc[full_data.Engulfing]
    cur_stat = EngulfingStatisticsOneSlice(data)
    summary_stats.loc[stat_names[i]] = cur_stat.loc[0]
    
    #7. 
    i = i+1
    data = full_data.loc[full_data.Continuation]
    cur_stat = EngulfingStatisticsOneSlice(data)
    summary_stats.loc[stat_names[i]] = cur_stat.loc[0]
    
    #8. 
    i = i+1
    data = full_data.loc[full_data.CloseContinuation]
    cur_stat = EngulfingStatisticsOneSlice(data)
    summary_stats.loc[stat_names[i]] = cur_stat.loc[0]
    
    #9. 
    i = i+1
    data = full_data.loc[full_data.HighLowContinuation]
    cur_stat = EngulfingStatisticsOneSlice(data)
    summary_stats.loc[stat_names[i]] = cur_stat.loc[0]
    
    #10. 
    i = i+1
    data = full_data.loc[full_data.Continuation==False]
    cur_stat = EngulfingStatisticsOneSlice(data)
    summary_stats.loc[stat_names[i]] = cur_stat.loc[0]
    
    #11. 
    i = i+1
    data = full_data.loc[full_data.CloseContinuation==False]
    cur_stat = EngulfingStatisticsOneSlice(data)
    summary_stats.loc[stat_names[i]] = cur_stat.loc[0]
    
    #12. 
    i = i+1
    data = full_data.loc[full_data.HighLowContinuation==False]
    cur_stat = EngulfingStatisticsOneSlice(data)
    summary_stats.loc[stat_names[i]] = cur_stat.loc[0]
    
    #13. 
    i = i+1
    data = full_data.loc[full_data.OppHighLow==True]
    cur_stat = EngulfingStatisticsOneSlice(data)
    summary_stats.loc[stat_names[i]] = cur_stat.loc[0]
    
    #14. 
    i = i+1
    data = full_data.loc[full_data.SmallBarPre==False]
    cur_stat = EngulfingStatisticsOneSlice(data)
    summary_stats.loc[stat_names[i]] = cur_stat.loc[0]
    
    
    
    return (summary_stats)

    

def EngulfingStatisticsOneTicker(ticker, period, pattern):
        #ticker: EURUSD, GOLD, etc. 
        #period: H1, D1, W1, etc. 
        #engulfing: if true runs on the engulfing statistics else runs on the outside bar statistics
        
        datafile_name = ticker + "_" + period + "_" + pattern + ".csv"
        statfile_name = ticker + "_" + period + "_" + pattern + "_summary.csv"
        
        data = pd.read_csv(MT5_Data_PATH + datafile_name, sep='\t', header=None, index_col=0,parse_dates=True, date_parser=custom_date_parser)
        col_names = ['Open', 'High','Low','Close','ATR', 'BullCandle', 'SmallBar', 'SmallBarPre', 'Engulfing', 'Outside', 'Inside', 'ReverseAfter', 
                     'N1_Open', 'N1_High', 'N1_Low','N1_Close','N2_Open', 'N2_High', 'N2_Low','N2_Close', 'Weekday']
        data.columns = col_names
        data.index.name = "DateTime"
        data = data.loc[data.index>cutoff_date,]
        
        # if the next bar is also bullish/bearish after a bullish/bearish engulfing
        data['Continuation'] = (data.BullCandle & (data.N1_Close > data.N1_Open)) | ((data.BullCandle == False)  & (data.N1_Close < data.N1_Open))
        data['Continuation2' ] = (data.BullCandle & (data.N2_Close > data.N2_Open)) | ((data.BullCandle == False)  & (data.N2_Close < data.N2_Open))
        # if the next bar closes higher/lower than the bullish/bearish engulfing bar. The next bar itself can be either bullish or bearish
        data['CloseContinuation'] = (data.BullCandle & (data.N1_Close > data.Close)) | ((data.BullCandle == False)  & (data.N1_Close < data.Close)) 
        # if the next bar has a  higher high/lower lower than the bullish/bearish engulfing bar. The next bar itself can be either bullish or bearish
        data['HighLowContinuation'] = (data.BullCandle & (data.N1_High > data.High)) | ((data.BullCandle == False)  & (data.N1_Low < data.Low)) 
        # Similar to the above, but compare the bar following next to the next bar after the engulfing bar 
        data['CloseContinuation2'] = (data.BullCandle & (data.N2_Close > data.N1_Close)) | ((data.BullCandle == False)  & (data.N2_Close < data.N1_Close)) 
        data['HighLowContinuation2'] = (data.BullCandle & (data.N2_High > data.N1_High)) | ((data.BullCandle == False)  & (data.N2_Low < data.N1_Low)) 
        # If the next bar made an opposite H/L move, ie.  for a bullish engulfing the following bar made a lower low for for a bearish engulfing, the following bar made a higher high
        data['OppHighLow'] = (data.BullCandle & (data.N1_Low < data.Low)) | ((data.BullCandle == False)  & (data.N1_High > data.High)) 
        pd.DataFrame.to_csv(data, Engulfing_Data_PATH +datafile_name)

        
        #1. Full Data Stat: 
        #total_data_rows = data.Close.count()
        summary_stats = EngulfingStatisticsOneDataBatch(data, pattern)
        
        #2. Bullish bars: 
            
        bull_data = data[data.BullCandle == True]
        summary_stats_bull = EngulfingStatisticsOneDataBatch(bull_data, pattern)
        #statfile_name_bull = ticker + "_" + period + "_" + ("Engulfing" if engulfing else "Outside") + "_bullbars_summary.csv"
        
        #pd.DataFrame.to_csv(summary_stats_bull, Engulfing_Summary_PATH + statfile_name_bull)
        summary_stats_bull.index = stat_names_bull
        
        #2. Bullish bars: 
        bear_data = data.loc[data.BullCandle == False]
        summary_stats_bear = EngulfingStatisticsOneDataBatch(bear_data, pattern)
        #statfile_name_bear = ticker + "_" + period + "_" + ("Engulfing" if engulfing else "Outside") + "_bearbars_summary.csv"
        #pd.DataFrame.to_csv(summary_stats_bear, Engulfing_Summary_PATH + statfile_name_bear)
        summary_stats_bear.index = stat_names_bear
        
        all_statistics = pd.concat([summary_stats, summary_stats_bull, summary_stats_bear])
        pd.DataFrame.to_csv(all_statistics, Engulfing_Summary_PATH + statfile_name)
        
        
        return(summary_stats)
        
        
 
def CrossSectionStats(period, pattern, stat_idx):
    output_data = pd.DataFrame(np.zeros((len(tickers+tickers_bull+tickers_bear),len(engulfing_stats_columns) )), index=tickers+tickers_bull+tickers_bear, columns = engulfing_stats_columns)
    
    print(stat_names[stat_idx])
    for i in range(len(tickers)):
        ticker = tickers[i]
        print(ticker)
        statfile_name = ticker + "_" + period + "_" + pattern +  "_summary.csv"
        summary_stats = pd.read_csv( Engulfing_Summary_PATH + statfile_name, header=0, index_col=0)
        output_data.loc[ticker] = summary_stats.loc[stat_names[stat_idx]]
    for  i in range(len(tickers)):
        ticker = tickers[i]
        print(ticker)
        statfile_name = ticker + "_" + period + "_" + pattern +  "_summary.csv"
        summary_stats = pd.read_csv( Engulfing_Summary_PATH + statfile_name, header=0, index_col=0)
        output_data.loc[tickers_bull[i]] = summary_stats.loc[stat_names_bull[stat_idx]]
    for  i in range(len(tickers)):
        ticker = tickers[i]
        print(ticker)
        statfile_name = ticker + "_" + period + "_" + pattern +  "_summary.csv"
        summary_stats = pd.read_csv( Engulfing_Summary_PATH + statfile_name, header=0, index_col=0)
        output_data.loc[tickers_bear[i]] = summary_stats.loc[stat_names_bear[stat_idx]]

    #print(output_data)
    return(output_data)

    
        

for ticker in tickers: 
    for period in periods: 
        for pattern in patterns:
            EngulfingStatisticsOneTicker(ticker, period, pattern)
            #print(ticker)




for i in range(len(stat_names)):
    for period in periods: 
        for pattern in patterns:
            #for bartype in bartypes: 
            ##if True: 
            print([stat_names[i], period, pattern])
            output_filename = Engulfing_CrossSectional_PATH + pattern + ("" if i==0 else  "_"+stat_names[i]) + "_"+ period + ".csv"
            data = CrossSectionStats (period, pattern,  i)
            pd.DataFrame.to_csv(data, output_filename)
        
    