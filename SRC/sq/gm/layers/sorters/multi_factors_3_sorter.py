from sq.gm.tools import *
from sq.layers import Sorter


class MultiFactors3Sorter(Sorter):
    """
    MultiFactors3Sorter filter and sort original targets.

    Main factors as follows:
    ----------------------
    - factor0~n, condition
    - get delta value of (factor0~n - TOTMKTCAP) OLS linear regression
    - sort by all delta values and beta/volatility/rsrs

    For example:
    ----------------------
    factor_dict = {
        "PETTM": "PETTM > 0",  # 市盈率TTM
        "ROEAVGCUT": "",  # 净资产收益率_平均(扣除非经常损益)
        "DY": "",  # 股息率(滚动12月-按证监会口径)
        "PB": "",  # 市净率(PB)
        "ROIC": "",  # 投入资本回报率
    }
    """

    def __init__(self, factor_dict: dict, weight: list):
        super().__init__()
        self._factor_dict = factor_dict
        self._weight = weight
        if factor_dict is None or len(factor_dict) < 2:
            raise ValueError("factor_dict needs 2 (key, value) pairs at least")

    @property
    def factor_dict(self):
        return self._factor_dict

    @property
    def weight(self):
        return self._weight

    def sort(self, in_list: list) -> list:
        symbol_list = list(in_list)
        df_with_factors = fast_batch_get_neutralized_factor2(symbol_list, self.now, self.factor_dict)

        beta = {}
        volatility = {}
        rsrs = {}
        for symbol in df_with_factors["symbol"].values:
            beta[symbol] = get_beta_weight_2(symbol, self.now, count=60)
            volatility[symbol] = get_volatility_normal(symbol, self.now, count=60)
            rsrs[symbol] = get_rsrs_weight(symbol, self.now)

        df = pd.DataFrame([])
        df["symbol"] = df_with_factors["symbol"]
        for factor, condition in self.factor_dict.items():
            df[factor] = df_with_factors[factor]
        df["beta"] = beta.values()
        df["volatility"] = volatility.values()
        df["rsrs"] = rsrs.values()

        all_weight = []
        all_weight.extend(self.weight)
        all_weight.extend([-1] * 3)
        symbol_list = get_symbol_list_by_weight_score(df, all_weight, start=1)
        return symbol_list


