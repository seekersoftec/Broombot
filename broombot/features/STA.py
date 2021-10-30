# import required modules
import btalib
import pandas as pd


def simple_technical_analyzer(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
        Simple Technical Analyzer
    """
    macd = btalib.macd(dataframe.close, pfast=7,
                       pslow=9, psignal=7)  # MACD(7,9,7)
    atr = btalib.atr(dataframe.high, dataframe.low,
                     dataframe.close, period=10)  # ATR(10)
    linearreg = btalib.linearreg(
        dataframe.close, period=10)  # LinearReg(period=10)
    # Bollinger bands(period=12, deviation=2.399)
    bbands = btalib.bbands(dataframe.close, period=12, devs=2.399)
    #
    # join the calculations as columns in original dataframe
    dataframe = dataframe.join([atr.df, linearreg.df, bbands.df, macd.df])
    second_last_row = dataframe.iloc[-2]
    print(second_last_row)
    #     indicator           signal     value
    # 0               RSI(14)             sell   40.1170
    # 1            STOCH(9,6)              buy   62.2920
    # 2          STOCHRSI(14)         oversold    0.0000
    # 3           MACD(12,26)             sell  -14.9800
    # 4               ADX(14)             sell   24.4420
    # 5           Williams %R             sell  -66.9920
    # 6               CCI(14)             sell -152.9455
    # 7               ATR(14)  less_volatility   47.3989
    # 8        Highs/Lows(14)             sell  -29.5598
    # 9   Ultimate Oscillator             sell   42.0320
    # 10                  ROC             sell   -2.5910
    # 11  Bull/Bear Power(13)             sell  -75.3000,
    new_dataframe = pd.DataFrame(names=['Indicator', 'signal', 'value'])
    # General interpretations of the MACD indicator are as follows:
    # Positive MACD = Increasing momentum of an uptrend (price rise),
    # Negative MACD = Increasing momentum of a downtrend (price fall),
    # If the MACD increases and crosses above the Signal Line, it is a bullish crossover,
    # If the MACD falls below the Signal Line, it is a bearish crossover.
    #
    # How to read ATR indicator. The average true range indicator looks like a single line in a section under your chart and the line can move up or down.
    # Reading the ATR indicator is not complicated: a higher ATR means increased volatility, while a lower ATR signals lower volatility.
    #
    # for the linear regression: check if the value is greater than or lesser than the last complete close price (if value is greater then uptrend)
    #
    # for the bbands: check if the mid is closer to the bottom or if it is closer to the top (closer to the top signifies an uptrend and closer to the bottom siginfies a downtrend)
    # if its in an average value then the market is sideways
    #

    return new_dataframe
