# # import required modules
# import time
# import datetime
# from binance.client import Client
# import os
# import requests
# import pandas as pd
# import numpy as np
# from cryptocmd import CmcScraper
# from enums import *

# #
# baseurl = "https://data.binance.vision/data/spot/monthly/klines"
# #
# symbol = 'BTCUSDT'
# interval = ''
# year = '2020'
# month = 9
# # file_name = "{}-{}-{}-{}.zip".format(symbol.upper(),
# #                                      interval, year, '{:02d}'.format(month))
# monthly_url = "https://data.binance.vision/data/spot/monthly/klines/BTCUSDT/1mo/BTCUSDT-1mo-2021-08.zip"
# daily_url = "https://data.binance.vision/data/spot/daily/klines/BTCUSDT/1m/BTCUSDT-1m-2021-09-17.zip"
# # url = "{0}/{1}/{2}/{3}-{4}-{5}-{6}.zip".format(
# #     baseurl, symbol, interval, symbol, interval, year, month)

# # read the dataset using the compression zip
# df = pd.read_csv(daily_url, names=["Open time", "Open", "High", "Low", "Close", "Volume", "Close time", "Quote asset volume",
#                                    "Number of trades", "Taker buy base asset volume", "Taker buy quote asset volume", "Ignore"], compression='zip')

# # display dataset
# print(df.head())


# #
# #

# YEARS = ['2017', '2018', '2019', '2020', '2021']
# INTERVALS = ["1m", "5m", "15m", "30m", "1h", "2h",
#              "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1mo"]
# DAILY_INTERVALS = ["1m", "5m", "15m", "30m",
#                    "1h", "2h", "4h", "6h", "8h", "12h", "1d"]
# TRADING_TYPE = ["spot", "um", "cm"]
# MONTHS = list(range(1, 13))
# MAX_DAYS = 35
# BASE_URL = 'https://data.binance.vision/'
# START_DATE = date(int(YEARS[0]), MONTHS[0], 1)
# END_DATE = datetime.date(datetime.now())
# #
# #


# # class BinanceDataVisionCollector:
# #     def __init__(self, trading_type: str, time_frame) -> None:
# #         self.BASE_URL = "https://data.binance.vision/data/"
# #         self.TRADING_TYPES = ["spot", "um", "cm"]
# #         self.NAMES = ["Open time", "Open", "High", "Low", "Close", "Volume", "Close time", "Quote asset volume",
# #                                    "Number of trades", "Taker buy base asset volume", "Taker buy quote asset volume", "Ignore"]
# #         self.time_frame = time_frame
# #         self.trading_type = trading_type.lower()

# #     @property
# #     def set_init_params(self) -> None:
# #         if (self.trading_type in self.TRADING_TYPES):
# #             pass
# #         else:
# #             pass
# #         return

# #     @property
# #     def get_all_symbols(self, type) -> list:
# #         if type == 'um':
# #             response = requests.get(
# #                 "https://fapi.binance.com/fapi/v1/exchangeInfo")
# #         elif type == 'cm':
# #             response = requests.get(
# #                 "https://dapi.binance.com/dapi/v1/exchangeInfo")
# #         else:
# #             response = requests.get(
# #                 "https://api.binance.com/api/v3/exchangeInfo")

# #         return list(map(lambda symbol: symbol['symbol'], json.loads(response)['symbols']))

# #     @property
# #     def get_monthly_data(self):
# #         return

# #     @property
# #     def get_daily_data(self):
# #         return

# #     def dataframe(self) -> pd.DataFrame:
# #         return


# # # Coinmarketcap
# # class Coinmarketcap:
# #     def __init__(self):
# #         pass

# #     def get_data(self, Coin="XRP", from_date="15-10-2017", to_date="25-10-2017"):
# #         # initialise scraper with time interval
# #         scraper = CmcScraper(Coin, from_date, to_date)

# #         # return dataframe for the data
# #         return scraper.get_dataframe()


# # # TA indicators
# # # lst = ["Accumulation/Distribution", "Accumulative Swing Index", "Advance/Decline", "Arnaud Legoux Moving Average", "Aroon", "Average Directional Index", "Average Price", "Average True Range", "Awesome Oscillator", "Balance of Power", "Bollinger Bands", "Bollinger Bands %B", "Bollinger Bands Width", "Chaikin Money Flow", "Chaikin Oscillator", "Chaikin Volatility", "Chande Kroll Stop", "Chande Momentum Oscillator", "Chop Zone", "Choppiness Index", "Commodity Channel Index", "Connors RSI", "Coppock Curve", "Correlation - Log", "Correlation Coefficient", "Detrended Price Oscillator", "Directional Movement", "Donchian Channels", "Double EMA", "EMA Cross", "Ease Of Movement", "Elder's Force Index", "Envelopes", "Fisher Transform", "Historical Volatility", "Hull Moving Average", "Ichimoku Cloud", "Keltner Channels", "Klinger Oscillator", "Know Sure Thing", "Least Squares Moving Average", "Linear Regression Curve", "Linear Regression Slope", "MA Cross", "MA with EMA Cross", "MACD", "Majority Rule", "Mass Index", "McGinley Dynamic", "Median Price", "Momentum",
# # #        "Money Flow Index", "Moving Average", "Moving Average Adaptive", "Moving Average Channel", "Moving Average Double", "Moving Average Exponential", "Moving Average Hamming", "Moving Average Modified", "Moving Average Multiple", "Moving Average Triple", "Moving Average Weighted", "Net Volume", "On Balance Volume", "Parabolic SAR", "Pivot Points Standard", "Price Channel", "Price Oscillator", "Price Volume Trend", "Rate Of Change", "Ratio", "Relative Strength Index", "Relative Vigor Index", "Relative Volatility Index", "SMI Ergodic Indicator/Oscillator", "Smoothed Moving Average", "Spread", "Standard Deviation", "Standard Error", "Standard Error Bands", "Stochastic", "Stochastic RSI", "SuperTrend", "TRIX", "Trend Strength Index", "Triple EMA", "True Strength Indicator", "Typical Price", "Ultimate Oscillator", "VWAP", "VWMA", "Volatility Close-to-Close", "Volatility Index", "Volatility O-H-L-C", "Volatility Zero Trend Close-to-Close", "Volume", "Volume Oscillator", "Vortex Indicator", "Williams %R", "Williams Alligator", "Williams Fractal", "Zig Zag"]
# # # curl -s -H 'Content-Type: application/json'  'https://scalpexindex.com/rest/price/BTCUSD?from=2021-07-19T22:41:48.000Z&to=2021-09-17T22:42:48.000Z&tg=1h'
# # # https://www.cryptodatadownload.com/data/binance/


# def GetHistoricalData(self, howLong):
#     self.howLong = howLong
#     # Calculate the timestamps for the binance api function
#     self.untilThisDate = datetime.datetime.now()
#     self.sinceThisDate = self.untilThisDate - \
#         datetime.timedelta(days=self.howLong)
#     # Execute the query from binance - timestamps must be converted to strings !
#     self.candle = self.client.get_historical_klines(
#         "BNBBTC", Client.KLINE_INTERVAL_1MINUTE, str(self.sinceThisDate), str(self.untilThisDate))

#     # Create a dataframe to label all the columns returned by binance so we work with them later.
#     self.df = pd.DataFrame(self.candle, columns=['dateTime', 'open', 'high', 'low', 'close', 'volume',
#                                                  'closeTime', 'quoteAssetVolume', 'numberOfTrades', 'takerBuyBaseVol', 'takerBuyQuoteVol', 'ignore'])
#     # as timestamp is returned in ms, let us convert this back to proper timestamps.
#     self.df.dateTime = pd.to_datetime(
#         self.df.dateTime, unit='ms').dt.strftime(Constants.DateTimeFormat)
#     self.df.set_index('dateTime', inplace=True)

#     # Get rid of columns we do not need
#     self.df = self.df.drop(['closeTime', 'quoteAssetVolume', 'numberOfTrades',
#                             'takerBuyBaseVol', 'takerBuyQuoteVol', 'ignore'], axis=1)

#     print(self.df)
