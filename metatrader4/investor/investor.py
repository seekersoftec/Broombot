#
# from DWX_ZeroMQ_Connector_v2_0_1_RC8 import *

# Initialize Connector
# _zmq = DWX_ZeroMQ_Connector()
#
#
"""
   string Publish_Symbols[9] = {
       "EURUSD","GBPUSD","USDJPY","USDCAD","AUDUSD","NZDUSD","USDCHF","XAUUSD","XAGUSD"
   };

  string Publish_Symbols[30] = {
       "EURUSD","EURGBP","EURAUD","EURNZD","EURJPY","EURCHF","EURCAD",
       "GBPUSD","AUDUSD","NZDUSD","USDJPY","USDCHF","USDCAD","GBPAUD",
   	"GBPNZD","GBPJPY","GBPCHF","GBPCAD","AUDJPY","CHFJPY","CADJPY",
   	"AUDNZD","AUDCHF","AUDCAD","NZDJPY","NZDCHF","NZDCAD","CADCHF",
   	"XAUUSD","XAGUSD"
   };
"""
#
#
# Publish_Symbols = ["EURUSD", "GBPUSD", "USDJPY", "USDCAD",
#                    "AUDUSD", "NZDUSD", "USDCHF", "XAUUSD", "XAGUSD"]
#
# Real-time BID/ASK prices
# for symbol in Publish_Symbols:
# _zmq._DWX_MTX_SUBSCRIBE_MARKETDATA_(symbol)
#
# _zmq._DWX_MTX_SUBSCRIBE_MARKETDATA_(Publish_Symbols[7])
# print(_zmq._Market_Data_DB)
#
#
# historical_data = _zmq._DWX_MTX_SEND_MARKETDATA_REQUEST_(
#     _symbol=Publish_Symbols[6], _timeframe=1440, _start='2020.01.04 17:00:00')
# print(historical_data)
#
#
# print(_zmq._DWX_MTX_SEND_MARKETDATA_REQUEST_(
#     _zmq._generate_default_data_dict()))
#
# print(_zmq._DWX_MTX_SEND_MARKETDATA_REQUEST_())
#
# self._Market_Data_DB
#


class Investor:
    def __init__(self) -> None:
        pass
    pass
