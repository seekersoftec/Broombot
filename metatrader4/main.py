
from libraries import DWX_ZeroMQ_Connector
#
from data import Investing
from analyzer import Analyzer
from investor import Investor

#

_CURRENCY = 'XAU/USD'
#
# Main function
#


def main():
    # Get data
    _data = Investing()
    search_result = _data.search(
        text=_CURRENCY, products=['currencies'], n_results=1)
    print(search_result)
    # #
    # historical_data = search_result.retrieve_historical_data(
    #     from_date='01/01/2016', to_date='01/01/2020')
    # print(historical_data)
    # #
    # #
    # technical_indicators = search_result.retrieve_technical_indicators(
    #     interval='1hour')
    # print(technical_indicators)
    #
    #
    #
    # Analyse data
    analysis = Analyzer(search_result)
    #
    # Invest
    investor = Investor()


if __name__ == '__main__':
    main()
