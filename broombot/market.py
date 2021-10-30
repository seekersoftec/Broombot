from collections import namedtuple
from datetime import datetime as dt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
#
from broombot.features.OBV import OBV
from broombot.features.RSI import RSI
from broombot.features.SMA import SMA
from broombot.features.SO import SO
#
import broombot.models.random_forest as rf
import broombot.models.deep_neural_network as dnn
#
from broombot.data import poloniex

# Enum-like object with 1:1 mapping.  Converts a readable
# market trend like 'bearish' to an int that is easier to parse.
TARGET_CODES = {'bearish': 0, 'neutral': 1, 'bullish': 2}


class Market:
    """ Evaluates TA indicators of a market

    Gets data from a market and then calculates technical analysis features.
    It also prepares this data to be fed into machine learning interfaces
    by creating a pandas DataFrame, and generating training/test sets
    for features (x-axis) and the target market trend (y-axis).

    Attributes:
        symbol: String of currency pair, like a ticker symbol.
        unit: String of time period unit for count argument.
            How far back to check historical market data.
            valid values: 'hour', 'day', 'week', 'month', 'year'
        count: Int of units.
            How far back to check historical market data.
        period: Int defining width of each chart candlestick in seconds.
            Valid values: 300, 900, 1800, 7200, 14400, 86400.
        json: JSON data as a list of dict dates, where the keys are
            the raw market statistics.
    """

    def __init__(self, json=None, symbol='USDT_BTC', unit='month', count=6, period=86400):
        """ Inits market class of symbol with data going back count units """
        self.symbol = symbol
        self.unit = unit
        self.count = count
        self.period = period

        if json is None:
            self.json = self.get_json()
        else:
            self.json = json

    def get_json(self):
        """ Gets market chart data from today to a previous date """
        today = dt.now()
        DIRECTION = 'last'
        epochs = date.get_end_start_epochs(today.year, today.month, today.day,
                                           DIRECTION, self.unit, self.count)
        return poloniex.chart_json(epochs['shifted'], epochs['initial'],
                                   self.period, self.symbol)[0]

    def set_features(self, partition=1):
        """ Parses market data JSON for technical analysis indicators

        Args:
            partition: Int of how many dates to take into consideration
                when evaluating technical analysis indicators.

        Returns:
            Pandas DataFrame instance with columns as numpy.float32 features.
        """
        if len(self.json) < partition + 1:
            raise ValueError(
                'Not enough dates for the specified partition size: {0}.  Try a smaller partition.'.format(partition))

        data = []
        for offset in range(len(self.json) - partition):
            json = self.json[offset: offset + partition]
            data.append(eval_features(json))
        return pd.DataFrame(data=data, dtype=np.float32)

    def set_long_features(self, features, columns_to_set=[], partition=2):
        """ Sets features of double the duration

        Example: Setting 14 day RSIs to longer will create add a
            feature column of a 28 day RSIs.

        Args:
            features: Pandas DataFrame instance with columns as numpy.float32 features.
            columns_to_set: List of strings of feature names to make longer
            partition: Int of how many dates to take into consideration
                when evaluating technical analysis indicators.

        Returns:
            Pandas DataFrame instance with columns as numpy.float32 features.
        """
        # Create long features DataFrame
        features_long = self.set_features(partition=2 * partition)

        # Remove features not specified by args.long
        unwanted_features = [
            f for f in features.columns if f not in columns_to_set]
        features_long = features_long.drop(unwanted_features, axis=1)

        # Prefix long columns with 'long_' to fix naming conflicts
        features_long.columns = ['long_{0}'.format(
            f) for f in features_long.columns]

        # Merge the two DataFrames
        skip = partition
        return pd.concat([features[skip:].reset_index(drop=True),
                          features_long],
                         axis=1)


def set_targets(x, delta=10):
    """ Sets target market trend for a date

    Args:
        x: Pandas DataFrame of market features
        delta: Positive number defining a price buffer between what is
            classified as a bullish/bearish market for the training set.
            delta is equivalent to the total size of the neutral price zone.
            delta / 2 is equivalent to either the positive or negative
            threshold of the neutral price zone.

    Returns:
        Pandas Series of numpy int8 market trend targets
    """
    data = []  # Keep track of targets
    for row, _ in x.iterrows():
        if row == x.shape[0] - 1:  # Can't predict yet, done.
            break

        # Get closing prices
        curr_close = x.close[row]
        next_close = x.close[row + 1]
        high_close = next_close + (delta / 2)  # Pos. neutral zone threshold
        low_close = next_close - (delta / 2)  # Neg. neutral zone threshold

        # Get target
        if curr_close < low_close:
            target = TARGET_CODES['bearish']
        elif curr_close > high_close:
            target = TARGET_CODES['bullish']
        else:
            target = TARGET_CODES['neutral']
        data.append(target)

    return pd.Series(data=data, dtype=np.int32, name='target')


def eval_features(json):
    """ Gets technical analysis features from market data JSONs

    Args:
        json: JSON data as a list of dict dates, where the keys are
            the raw market statistics.

    Returns:
        Dict of market features and their values
    """
    return {'close': json[-1]['close'],
            'sma': SMA.eval_from_json(json),
            'rsi': RSI.eval_from_json(json),
            'so': SO.eval_from_json(json),
            'obv': OBV.eval_from_json(json)}


def target_code_to_name(code):
    """ Converts an int target code to a target name

    Since self.TARGET_CODES is a 1:1 mapping, perform a reverse lookup
    to get the more readable name.

    Args:
        code: Value from self.TARGET_CODES

    Returns:
        String target name corresponding to the given code.
    """
    TARGET_NAMES = {v: k for k, v in TARGET_CODES.items()}
    return TARGET_NAMES[code]


def setup_model(x, y, model_type='random_forest', seed=None, **kwargs):
    """ Initializes a machine learning model

    Args:
        x: Pandas DataFrame, X axis of features
        y: Pandas Series, Y axis of targets
        model_type: Machine Learning model to use
            Valid values: 'random_forest'
        seed: Random state to use when splitting sets and creating the model
        **kwargs: Scikit Learn's RandomForestClassifier kwargs

    Returns:
        Trained model instance of model_type
    """
    assert len(x) > 1 and len(
        y) > 1, 'Not enough data objects to train on (minimum is at least two, you have (x: {0}) and (y: {1}))'.format(len(x), len(y))

    sets = namedtuple('Datasets', ['train', 'test'])
    x_train, x_test, y_train, y_test = train_test_split(x,
                                                        y,
                                                        random_state=seed,
                                                        shuffle=False)
    x = sets(x_train, x_test)
    y = sets(y_train, y_test)

    if model_type == 'random_forest' or model_type == 'rf':
        model = rf.RandomForest(x, y, random_state=seed, **kwargs)
    elif model_type == 'deep_neural_network' or model_type == 'dnn':
        model = dnn.DeepNeuralNetwork(x, y, **kwargs)
    else:
        raise ValueError('Invalid model type kwarg')
    return model
