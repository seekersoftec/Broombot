import investpy


#
# Data from investing.com
#


class Investing:
    """
        Data from Investing.com
    """

    def __init__(self):
        self.kl = ''
        pass

    def search(self):
        investpy.search_quotes(text='apple', products=['stocks'],
                               countries=['united states'], n_results=1)
        pass

    def get_historical_data(self):
        investpy.get_stock_historical_data(stock='XAU',
                                           country='United States',
                                           from_date='01/01/2010',
                                           to_date='01/01/2020')
        pass
    pass


# df = investpy.get_stock_historical_data(stock='XAU',
#                                         country='United States',
#                                         from_date='01/01/2010',
#                                         to_date='01/01/2020')

# print(df.head())

search_result = investpy.search_quotes(
    text='xau/usd', products=['currencies'], n_results=1)
print(search_result)
#
recent_data = search_result.retrieve_recent_data()
print(recent_data)
#
# historical_data = search_result.retrieve_historical_data(
#     from_date='01/01/2019', to_date='01/01/2020')
# print(historical_data)
#
information = search_result.retrieve_information()
print(information)
#
# default_currency = search_result.retrieve_currency()
# print(default_currency)
#
intervals = ['1min', '5mins', '15mins', '30mins',
             '1hour', '5hours', 'daily', 'weekly', 'monthly']
technical_indicators = search_result.retrieve_technical_indicators(
    interval='1hour')
print(technical_indicators)
