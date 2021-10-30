import pandas as pd
import btalib
import abc


class TechnicalAnalysis(abc.ABC):
    """ Abstract class for calculating technical analysis indicators """

    @staticmethod
    @abc.abstractmethod
    def eval_algorithm(*args, **kwargs):
        """ Evaluates TA algorithm """

    @staticmethod
    @abc.abstractmethod
    def eval_from_json(json):
        """ Evaluates TA algorithm from JSON

        Args:
            json: List of dates where each entry is a dict of raw market data.
        """


# On Balance Volume
# Relative Strength Index
# Simple Moving Average
# Stochastic Oscillator
#
#
#
# import required modules


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
# Read a csv file into a pandas dataframedropna(axis=1)
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
# ta_analyzer = TechnicalAnalyser(df)
# ini = ta_analyzer.eval_indicators()
# print(ini.columns)
# print(ini['signal'].tail(5))


# # Price Transform
# from .price import *  # noqa: F401 F403

# # Math Operators
# from .mathop import *  # noqa: F401 F403

# # Math Transform
# from .math import *  # noqa: F401 F403

# # Utils
# from .crossover import *  # noqa: F401 F403

# # Overlap
# from .ewma import *  # noqa: F401 F403

# from .sma import *  # noqa: F401 F403
# from .ema import *  # noqa: F401 F403
# from .smma import *  # noqa: F401 F403
# from .wma import *  # noqa: F401 F403

# from .dema import *  # noqa: F401 F403
# from .kama import *  # noqa: F401 F403
# from .tema import *  # noqa: F401 F403
# from .trima import *  # noqa: F401 F403
# from .trix import *  # noqa: F401 F403
# from .t3 import *  # noqa: F401 F403

# from .mavp import *  # noqa: F401 F403

# from .mama import *  # noqa: F401 F403
# from .ht_trendline import *  # noqa: F401 F403

# # ## overlap non-ma
# from .midpoint import *  # noqa: F401 F403

# # Cycle
# from .ht_dcperiod import *  # noqa: F401 F403
# from .ht_dcphase import *  # noqa: F401 F403
# from .ht_phasor import *  # noqa: F401 F403
# from .ht_sine import *  # noqa: F401 F403
# from .ht_trendmode import *  # noqa: F401 F403

# # Statistics
# from .beta import *  # noqa: F401 F403
# from .correl import *  # noqa: F401 F403
# from .linreg import *  # noqa: F401 F403
# from .madev import *  # noqa: F401 F403
# from .stddev import *  # noqa: F401 F403
# from .var import *  # noqa: F401 F403

# # ## Overlap - depends on stddev
# from .bbands import *  # noqa: F401 F403

# # Volatility
# from .atr import *  # noqa: F401 F403

# # Momentum
# from .aroon import *  # noqa: F401 F403
# from .bop import *  # noqa: F401 F403
# from .cci import *  # noqa: F401 F403
# from .cmo import *  # noqa: F401 F403
# from .directionalmove import *  # noqa: F401 F403
# from .macd import *  # noqa: F401 F403
# from .mfi import *  # noqa: F401 F403
# from .mom import *  # noqa: F401 F403
# from .ppo import *  # noqa: F401 F403
# from .roc import *  # noqa: F401 F403
# from .rsi import *  # noqa: F401 F403
# from .sar import *  # noqa: F401 F403
# from .sarext import *  # noqa: F401 F403
# from .stochastic import *  # noqa: F401 F403
# from .stochrsi import *  # noqa: F401 F403
# from .williamsr import *  # noqa: F401 F403
# from .ultimateoscillator import *  # noqa: F401 F403

# # Volume
# from .ad import *  # noqa: F401 F403
# from .obv import *  # noqa: F401 F403

groups = ['price', 'overlap', 'momentum',
          'cycle', 'statistic', 'volatility', 'volume']
inds = btalib.get_ind_by_group()
print(inds[groups[2]])


# print(btalib.get_groups())
# Index(['acos', 'ad', 'adosc', 'apo', 'asin', 'atan', 'bot', 'ceil', 'close',
#        'close_time', 'cmo', 'cos', 'cosh', 'dema', 'ema', 'ewma', 'exp',
#        'floor', 'gd', 'high', 'histogram', 'ignore', 'intercept', 'linreg',
#        'ln', 'log10', 'low', 'macd', 'max', 'maxindex', 'meandev', 'mid',
#        'midpoint', 'min', 'minindex', 'mom', 'open', 'ppo', 'quote_av', 'roc',
#        'rocp', 'rocr', 'rocr100', 'rsi', 'signal', 'sin', 'sinh', 'slope',
#        'sma', 'smma', 'sqrt', 'std', 'stochrsi', 'sum', 't3', 'tan', 'tanh',
#        'tb_base_av', 'tb_quote_av', 'tema', 'top', 'trades', 'trima', 'trix',
#        'tsf', 'var', 'volume', 'wma'],
#       dtype='object')
