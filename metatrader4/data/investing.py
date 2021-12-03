#
import investpy


#
# Data from investing.com
#


class Investing:
    """
        Generic class to get data from Investing.com
    """

    def __init__(self):
        self.TIME_FRAMES = ['1min', '5mins', '15mins', '30mins',
                            '1hour', '5hours', 'daily', 'weekly', 'monthly']
        self.CURRENCY_TYPES = {
            'stocks': [
                'get_stocks', 'get_stocks_list', 'get_stocks_dict',
                'get_stock_countries', 'get_stock_recent_data',
                'get_stock_historical_data', 'get_stock_company_profile',
                'get_stock_dividends', 'get_stock_information',
                'get_stocks_overview', 'get_stock_financial_summary', 'search_stocks'
            ],
            'funds': [
                'get_funds', 'get_funds_list', 'get_funds_dict',
                'get_fund_countries', 'get_fund_recent_data', 'get_fund_historical_data',
                'get_fund_information', 'get_funds_overview', 'search_funds'
            ],
            'etfs': [
                'get_etfs', 'get_etfs_list', 'get_etfs_dict',
                'get_etf_countries', 'get_etf_recent_data',
                'get_etf_historical_data', 'get_etf_information',
                'get_etfs_overview', 'search_etfs'
            ],
            'indices': [
                'get_indices', 'get_indices_list',
                'get_indices_dict', 'get_index_countries',
                'get_index_recent_data', 'get_index_historical_data',
                'get_index_information', 'get_indices_overview', 'search_indices'
            ],
            'currency_crosses': [
                'get_currency_crosses', 'get_currency_crosses_list', 'get_currency_crosses_dict',
                'get_available_currencies', 'get_currency_cross_recent_data', 'get_currency_cross_historical_data',
                'get_currency_cross_information', 'get_currency_crosses_overview', 'search_currency_crosses'
            ],
            'bonds': [
                'get_bonds', 'get_bonds_list', 'get_bonds_dict',
                'get_bond_countries', 'get_bond_recent_data',
                'get_bond_historical_data', 'get_bond_information',
                'get_bonds_overview', 'search_bonds'

            ],
            'commodities': [
                'get_commodities', 'get_commodities_list', 'get_commodities_dict', 'get_commodity_groups',
                'get_commodity_recent_data', 'get_commodity_historical_data', 'get_commodity_information', 'get_commodities_overview',
                'search_commodities'
            ],
            'crypto': [
                'get_cryptos', 'get_cryptos_list', 'get_cryptos_dict', 'get_crypto_recent_data',
                'get_crypto_historical_data', 'get_crypto_information', 'get_cryptos_overview', 'search_cryptos'
            ],
            'certificates': [
                'get_certificates', 'get_certificates_list', 'get_certificates_dict', 'get_certificate_countries',
                'get_certificate_recent_data', 'get_certificate_historical_data', 'get_certificate_information', 'get_certificates_overview',
                'search_certificates'
            ]
        }

    def search(self, **kwargs):
        """
            search(text='apple', products=['stocks'],
                countries=['united states'], n_results=1)
        """

        return investpy.search_quotes(**kwargs)

    def get_historical_data(self, _currency_type='STOCKS', **kwargs):
        """
            Get Historical data (not working yet)
        """
        # investpy.get_stock_historical_data(stock='XAU',
        #                                    country='United States',
        #                                    from_date='01/01/2010',
        #                                    to_date='01/01/2020')
        if (self.CURRENCY_TYPES[_currency_type.lower()]):
            self.CURRENCY_TYPES[_currency_type.lower()]

           # new Function('return ' + fn_string)();
        return investpy.get_stock_historical_data(**kwargs)


# if __name__ == '__main__':

    # df = investpy.get_stock_historical_data(stock='XAU',
    #                                         country='United States',
    #                                         from_date='01/01/2010',
    #                                         to_date='01/01/2020')
    #
    # print(df.head())

    # investing = Investing()
    # search_result = investing.search(
    #     text='xau/usd', products=['currencies'], n_results=1)
    # print(search_result)
    #
    # recent_data = search_result.retrieve_recent_data()
    # print(recent_data)
    #
    # historical_data = search_result.retrieve_historical_data(
    #     from_date='01/01/2019', to_date='01/01/2020')
    # print(historical_data)
    #
    # information = search_result.retrieve_information()
    # print(information)
    #
    # default_currency = search_result.retrieve_currency()
    # print(default_currency)
    #

    # technical_indicators = search_result.retrieve_technical_indicators(
    #     interval='1hour')
    # print(technical_indicators)
    #
    #


#
#
# from .search import search_quotes
# # from .search import search_events

# from .news import economic_calendar

# from .technical import technical_indicators, moving_averages, pivot_points

#
