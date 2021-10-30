
#
# OANDA
from oandapyV20 import API
from custom_classes import Run, os
#
#
# #
# oanda_access_token = 'e353c285b941690a0fcb89e4da1b4aa4-f67670c87c242e1ad0d5a4c45ac31104'
# oanda_client = API(access_token=oanda_access_token)


# def get_historical_data_from_oanda(oanda_client: API, instrument: list = ['XAU_USD'], timer: list = [1800, 86400]):
#     """
#         Get historical data from oanda
#     """

#     # 'Note however that this may be time consuming as the dataset is huge
#     CandlestickGranularity_ = [{
#         "M15": "15 minute candlesticks, hour alignment",
#         "M30": "30 minute candlesticks, hour alignment",
#         "H1": "1 hour candlesticks, hour alignment",
#         "H2": "1 hour candlesticks, day alignment",
#         "H3": "3 hour candlesticks, day alignment",
#         "H4": "4 hour candlesticks, day alignment",
#         "H6": "6 hour candlesticks, day alignment",
#         "H8": "8 hour candlesticks, day alignment",
#         "H12": "12 hour candlesticks, day alignment",
#     },
#         {
#         "D": "1 day candlesticks, day alignment",
#         "W": "1 week candlesticks, aligned to start of week",
#     }]
#     # format timeframe
#     _from_gr = '2019-03-01T00:00:00Z'
#     _end_gr = datetime.datetime.utcnow().isoformat('T')+'Z'
#     _end_gr = str(_end_gr[:-8] + 'Z')
#     #
#     _from = '2017-01-01T00:00:00Z'
#     _end = datetime.datetime.utcnow().isoformat('T')+'Z'
#     _end = str(_end[:-8] + 'Z')
#     #
#     time_frame = [[_from_gr, _end_gr], [_from, _end]]
#     # download data
#     Run(instrument=instrument, timeframe=time_frame, api=oanda_client,
#         granular=CandlestickGranularity_, timer=timer)
