#import libraries
import pandas as pd
import pandas_datareader.data as pdr
import datetime
start = datetime.datetime(2020,2,19)
end = datetime.datetime(2021,2,18)
df = pdr.DataReader('BTC-USD','yahoo',start,end)
print(df.head())