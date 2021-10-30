from speculator.features.TechnicalAnalysis import TechnicalAnalysis
from speculator.data import poloniex


class SO(TechnicalAnalysis):
    """
    Stochastic Oscillator:
    %K = 100 * (C - L(t)) / (H14 - L(t))
        such that,
            C = Current closing Price
            L(t) = Lowest Low over some duration t
            H(t) = Highest High over some duration t
              * t is usually 14 days

    %K follows the speed/momentum of a price in a market
    """

    def eval_algorithm(closing, low, high):
        """ Evaluates the SO algorithm

        Args:
            closing: Float of current closing price.
            low: Float of lowest low closing price throughout some duration.
            high: Float of highest high closing price throughout some duration.

        Returns:
            Float SO between 0 and 100.
        """
        if high - low == 0:  # High and low are the same, zero division error
            return 100 * (closing - low)
        else:
            return 100 * (closing - low) / (high - low)

    def eval_from_json(json):
        """ Evaluates SO from JSON (typically Poloniex API response)

        Args:
            json: List of dates where each entry is a dict of raw market data.

        Returns:
            Float SO between 0 and 100.
        """
        close = json[-1]['close']  # Latest closing price
        low = min(poloniex.get_attribute(json, 'low'))  # Lowest low
        high = max(poloniex.get_attribute(json, 'high'))  # Highest high
        return SO.eval_algorithm(close, low, high)
