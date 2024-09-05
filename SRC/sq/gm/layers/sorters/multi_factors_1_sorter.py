from sq.gm.tools import *
from sq.layers import Sorter


class MultiFactors1Sorter(Sorter):
    """
    MultiFactors1Sorter filter and sort original targets.

    Main factors as follows:
    ----------------------
    - ROE/ROIC 's std < the setpoint。
    - PETTM, 11 < PETTM  < 27
    - NPGRT, 10 < NPGRT < 39
    - TAGRT, 10 < TAGRT < 39
    """

    def __init__(self, count=14, std=0.11):
        super().__init__()
        self._count = count
        self._std = std

    @property
    def count(self):
        return self._count

    @property
    def std(self):
        return self._std

    def sort(self, in_list: list) -> list:
        symbol_list = list(in_list)
        last_day = get_previous_trading_date("SHSE", self.now)
        # 第一步：获取ROE/ROIC的std
        symbol_ROE_ROIC_list = get_roe_roic_list(symbol_list, last_day, self.count, self.std)
        # 第二步：这里假设PETTM在正常水平，即 11 < PETTM  < 27
        # 第三步：NPGRT  TAGRT
        factor_dict = {
            "PETTM": "PETTM > 11 and PETTM < 27",
            "TAGRT": "TAGRT > 10 and TAGRT < 39",
            "NPGRT": "NPGRT > 10 and NPGRT < 39",
        }
        df = get_fundamentals_n_without_limit3(symbols=symbol_ROE_ROIC_list, end_date=last_day,
                                               fields_and_filter=factor_dict, df=True)

        df = df.dropna()
        # symbol_list = get_symbol_list_by_delta_value(df, ["ROE"], "PB", "symbol")
        df = df.sort_values(["PETTM"])
        return list(df["symbol"].to_list())


