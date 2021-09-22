# import required modules
import abc
import btalib

import pandas as pd

#
#

# TA master analyser
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
print(indicators[0].__doc__)

# print(df.tail(5))
#
#
#
#


class TechnicalAnalyser():
    """ class for calculating technical analysis indicators """

    def __init__(self):
        super().__init__()

    def eval_algorithm(self, **kwargs):
        """ Evaluates TA algorithm """
        return

#
#


class TechnicalAnalysis(abc.ABC):
    """ Abstract class for calculating technical analysis indicators """

    @staticmethod
    @abc.abstractmethod
    def eval_algorithm(*args, **kwargs):
        """ Evaluates TA algorithm """

    @staticmethod
    @abc.abstractmethod
    def eval_from_dataframe(dataframe):
        """ Evaluates TA algorithm from JSON

        Args:
            json: List of dates where each entry is a dict of raw market data.
        """
