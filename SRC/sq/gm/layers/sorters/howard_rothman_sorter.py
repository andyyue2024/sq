from sq.gm.tools import *
from sq.layers import Sorter


class HowardRothmanSorter(Sorter):
    """
    HowardRothmanSorter filter and sort original targets.

    Main factors as follows:
    ----------------------
    - 总市值≧市场平均值*1.0. TOTMKTCAP	总市值
    - 最近一季流动比率≧市场平均值。  PCTTM	市现率TTM
    - 近四季营收成长率介于6%至30%。 NPGRT	归属母公司净利润增长率。由高到低
    - 近四季盈余成长率介于8%至50%。 TAGRT	营业总收入增长率。由高到低
    - ROEAVGCUT	净资产收益率_平均(扣除非经常损益)
    - FCFEPS 每股股东自由现金流量
    Sort by:
    ----------------------
    - weight score of ROEAVGCUT and FCFEPS

    """

    def __init__(self):
        super().__init__()

    def sort(self, in_list: list) -> list:
        symbol_list = list(in_list)
        factor_dict = {
            "TOTMKTCAP": "",
            "PCTTM": "",
        }
        df = get_fundamentals_n_without_limit3(symbols=symbol_list, end_date=self.now, fields_and_filter=factor_dict, df=True)
        TOTMKTCAP_mean = df["TOTMKTCAP"].mean()
        PCTTM_mean = df["PCTTM"].mean()
        df = df[df["TOTMKTCAP"] > TOTMKTCAP_mean]
        df = df[df["PCTTM"] > PCTTM_mean]
        symbol_list = []
        symbol_list.extend(df["symbol"].values)
        if len(symbol_list) <= 0:
            return symbol_list

        factor_dict = {
            "NPGRT": "NPGRT > 6 and NPGRT < 30",
            "TAGRT": "TAGRT > 8 and TAGRT < 50",
            "ROEAVGCUT": "",
            "FCFEPS": "",
        }
        df = get_fundamentals_n_without_limit3(symbols=symbol_list, end_date=self.now, fields_and_filter=factor_dict, df=True)
        ROEAVGCUT_mean = df["ROEAVGCUT"].mean()
        FCFEPS_mean = df["FCFEPS"].mean()

        df_new = pd.DataFrame([])
        df_new["symbol"] = df["symbol"]
        # df_new["NPGRT"] = df["NPGRT"]
        # df_new["TAGRT"] = df["TAGRT"]
        df_new["ROEAVGCUT"] = df["ROEAVGCUT"].fillna(ROEAVGCUT_mean)
        df_new["FCFEPS"] = df["FCFEPS"].fillna(FCFEPS_mean)

        # weight = [-1, -1, -1, -1]
        weight = [-1, -1]
        symbol_list = get_symbol_list_by_weight_score(df_new, weight, start=1)
        return symbol_list


