from sq.gm.tools import *
from sq.layers import Sorter


class MultiFactors2Sorter(Sorter):
    """
    MultiFactors2Sorter filter and sort original targets.

    Main factors as follows:
    ----------------------
    - factor0, condition
    - factor1~n, conditions
    - sort by delta value of (factor0 - factor1~n) OLS linear regression

    For example:

    factor_dict = {
            "PB": "PB > 0",
            "ROEAVG": "ROEAVG > 0",
            # "EBITMARGIN": "",
        }
    """

    def __init__(self, factor_dict: dict):
        super().__init__()
        self._factor_dict = factor_dict
        if factor_dict is None or len(factor_dict) < 2:
            raise ValueError("factor_dict needs 2 (key, value) pairs at least")

    @property
    def factor_dict(self):
        return self._factor_dict

    def sort(self, in_list: list) -> list:
        last_day = get_previous_trading_date("SHSE", self.now)
        symbol_list = list(in_list)
        keys = set(self.factor_dict.keys())
        main_key = keys.pop()  # axis Y

        df = pd.DataFrame([])
        df["symbol"] = symbol_list
        df = get_fundamentals_without_limit3(symbols=symbol_list, start_date=last_day, end_date=last_day,
                                             fields_and_filter=self.factor_dict, df=True)
        df = df.dropna()
        symbol_list = get_symbol_list_by_delta_value(df, list(keys), main_key, "symbol")
        return symbol_list


