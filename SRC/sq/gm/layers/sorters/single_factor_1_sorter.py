from sq.gm.tools import *
from sq.layers import Sorter


class SingleFactor1Sorter(Sorter):
    """
    SingleFactor1Sorter filter and sort original targets.

    Main factors as follows:
    ----------------------
    - factor0, condition。
    - sort by value of factor0
    """

    def __init__(self, factor, ascending=False):
        super().__init__()
        self._factor = factor
        self._ascending = ascending

    @property
    def factor(self):
        return self._factor

    @property
    def ascending(self):
        return self._ascending

    def sort(self, in_list: list) -> list:
        symbol_list = list(in_list)
        last_day = get_previous_trading_date("SHSE", self.now)
        factor_dict = {
            self.factor: "",
        }
        df = get_fundamentals_n_without_limit3(symbols=symbol_list, end_date=last_day,
                                               fields_and_filter=factor_dict, df=True)

        df = df.dropna()
        df = df.sort_values([self.factor], ascending=self.ascending)
        return list(df["symbol"].to_list())


