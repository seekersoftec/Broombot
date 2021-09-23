# import required modules
import btalib
import pandas as pd


class TechnicalAnalyser:
    """
        Technical Analysis master analyser
        Class for calculating technical analysis indicators.

        Get technical analyses based on 100+(120) indicators,
        56 canlestick pattern detectors and 32 strategy alerts.
    """

    def __init__(self, dataframe: pd.DataFrame) -> None:
        self.dataframe = dataframe
        self.ohlcv = ['open', 'high', 'low', 'close', 'volume']
        # Filter some indicators
        self.filtered_indicators = []
        for indicator in btalib.get_indicators():
            # print(getattr(indicator, 'alias', ())[0])
            for input_val in getattr(indicator, 'inputs', ()):
                if input_val in self.ohlcv:
                    self.filtered_indicators.append(indicator)

    def eval_indicators(self, **kwargs) -> pd.DataFrame:
        """ Evaluates TA algorithms and returns a dataframe """
        for indicator in self.filtered_indicators:
            try:
                self.dataframe = self.dataframe.combine_first(
                    indicator(self.dataframe).df)
            except Exception:
                pass
        return self.dataframe


#
#
#
#
# Read a csv file into a pandas dataframe
df = pd.read_csv('data/BTCUSDT-1d-binance_data.csv',
                 parse_dates=True, index_col='timestamp')
df.index = pd.to_datetime(df.index, unit='ms')
#
#
# create sma and attach as column to original df
# df['20sma'] = btalib.sma(df.close, period=20).df
#
# rsi = btalib.rsi(df, period=14).df
# # print(rsi.df.rsi[-1])
# macd = btalib.macd(df, pfast=20, pslow=50, psignal=13).df
# df = df.join([rsi, macd])
#
#
ta_analyzer = TechnicalAnalyser(df)
ini = ta_analyzer.eval_indicators()
print(ini.tail(5))
