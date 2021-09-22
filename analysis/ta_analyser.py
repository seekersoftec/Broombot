# import required modules
import btalib
import pandas as pd

#
#
#

#
#
# Read a csv file into a pandas dataframe
df = pd.read_csv('../data/BTCUSDT-1d-binance_data.csv',
                 parse_dates=True, index_col='timestamp')
# df.index = pd.to_datetime(df.index, unit='ms')
# create sma and attach as column to original df
df['20sma'] = btalib.sma(df.close, period=20).df

rsi = btalib.rsi(df, period=14).df
# print(rsi.df.rsi[-1])
macd = btalib.macd(df, pfast=20, pslow=50, psignal=13).df
df = df.join([rsi, macd])

#
#
indicators = btalib.get_indicators()
# ac = indicators[0](df)
# print(indicators[0].__doc__)

# print(df.tail(5))
#
#
#
#

#
# TA master analyser
#


class TechnicalAnalyser():
    """ class for calculating technical analysis indicators """

    def __init__(self, dataframe: pd.DataFrame):
        pass

    def eval(self, **kwargs) -> pd.DataFrame:
        """ Evaluates TA algorithms and returns a dataframe """
        return


#
