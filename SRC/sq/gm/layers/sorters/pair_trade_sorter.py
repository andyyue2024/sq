from sq.gm.tools import *
from sq.layers import Sorter


class PairTradeSorter(Sorter):
    """
    PairTradeSorter filter and sort original targets.

    Main factors as follows:
    ----------------------
    - sort by d_value of (close1 - close0) OLS linear regression
    - symbol_1 when d_value > mean + 3 * std
    - symbol_2 when d_value < mean - 3 * std
    """

    def __init__(self, symbol_1: str = "SHSE.601939", symbol_2: str = "SHSE.601288",
                 weight=0.481477, bias=0.481829, mean=-0.000203539120501, std=0.0754807889752):
        super().__init__()
        self.symbol_1 = symbol_1
        self.symbol_2 = symbol_2
        self.weight = weight
        self.bias = bias
        self.mean = mean
        self.std = std

        self.flagX = False
        self.flagY = False

    def sort(self, in_list: list) -> list:
        # symbol_list = list(in_list)
        last_day = get_previous_trading_date(exchange='SHSE', date=self.now)
        df1 = history(self.symbol_1, frequency="1d", start_time=last_day
                      , end_time=last_day, fields="close", fill_missing="last", adjust=ADJUST_PREV, df=True)
        df2 = history(self.symbol_2, frequency="1d", start_time=last_day,
                      end_time=last_day, fields="close", fill_missing="last", adjust=ADJUST_PREV, df=True)
        df1 = df1["close"].values
        df2 = df2["close"].values

        d_value = df2 - (df1 * self.weight + self.bias)
        if (self.flagX and d_value < self.mean + self.std) or (
                self.flagY and d_value > self.mean - self.std):
            self.flagX = False
            self.flagY = False
            return []
        if d_value > self.mean + 3 * self.std:
            self.flagX = True
            return [self.symbol_1]
        if d_value < self.mean - 3 * self.std:
            self.flagY = True
            return [self.symbol_2]
        return []
