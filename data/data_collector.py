# import required modules
import time
import math
import os
import os.path
import pandas as pd
from binance.client import Client
from datetime import timedelta, datetime
from dateutil import parser


class BinanceCollector:
    """
        Binance Data Collector
    """

    def __init__(self, api_key: str, api_secret: str, data_dir: str = '', batch_size: int = 750) -> None:
        self.binance_api_key = api_key
        self.binance_api_secret = api_secret
        self.data_dir = data_dir
        self.batch_size = batch_size
        # valid intervals - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
        self.binsizes = {"1m": 1, "3m": 3, "5m": 5, "15m": 15, "30m": 30, "1h": 60, "2h": 120,
                         "4h": 240, "6h": 360, "8h": 480, "12h": 720, "1d": 1440, "3d": 4320, "1w": 10080, "1M": 40320}

        self.binance_client = Client(
            api_key=self.binance_api_key, api_secret=self.binance_api_secret)

    #
    def __minutes_of_new_data(self, symbol: str, kline_size: str, data: pd.DataFrame, source: str) -> tuple:
        """
            Calculates the date and time of data And adds new data accordingly 
        """
        if len(data) > 0:
            old = parser.parse(data["timestamp"].iloc[-1])
        elif source == "binance":
            old = datetime.strptime('1 Jan 2017', '%d %b %Y')
        if source == "binance":
            new = pd.to_datetime(self.binance_client.get_klines(
                symbol=symbol, interval=kline_size)[-1][0], unit='ms')
        return old, new

    def get_all_pairs(self) -> list:
        """
            Get all pairs
        """
        exchange_info = self.binance_client.get_exchange_info()
        symbols = []
        for symbol in exchange_info['symbols']:
            if (symbol['symbol'] != None):
                symbols.append(symbol['symbol'])
        return symbols

    #
    #
    def get_historical_data(self, symbol: str, kline_size: str, save: bool = False) -> pd.DataFrame:
        """
            Get All the historical data from binance
        """
        filename = self.data_dir + \
            '%s-%s-binance_data.csv' % (symbol, kline_size)
        #
        #
        if os.path.isfile(filename):
            data_df = pd.read_csv(filename)
        else:
            data_df = pd.DataFrame()
        oldest_point, newest_point = self.__minutes_of_new_data(
            symbol, kline_size, data_df, source="binance")
        delta_min = (newest_point - oldest_point).total_seconds()/60
        available_data = math.ceil(delta_min/self.binsizes[kline_size])
        #
        #
        # if oldest_point == datetime.strptime('1 Jan 2017', '%d %b %Y'):
        #     print('Downloading all available %s data for %s from binance. Be patient..!' % (
        #         kline_size, symbol))
        # else:
        #     print('Downloading %d minutes of new data available for %s, i.e. %d instances of %s data.' % (
        #         delta_min, symbol, available_data, kline_size))
        #
        klines = self.binance_client.get_historical_klines(symbol, kline_size, oldest_point.strftime(
            "%d %b %Y %H:%M:%S"), newest_point.strftime("%d %b %Y %H:%M:%S"))
        data = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close',
                                             'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore'])
        data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
        #
        # convert
        # data[['open', 'high', 'low', 'close']] = data[[
        # 'open', 'high', 'low', 'close']].astype(float).div(100).round(2)
        #
        #
        if len(data_df) > 0:
            temp_df = pd.DataFrame(data)
            data_df = data_df.append(temp_df)
        else:
            data_df = data
        data_df.set_index('timestamp', inplace=True)
        #
        #
        if save:
            data_df.to_csv(filename)

        # print('All caught up..!')

        return data_df
