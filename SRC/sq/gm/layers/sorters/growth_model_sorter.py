from sq.gm.tools import *
from sq.layers import Sorter


class GrowthModelSorter(Sorter):
    """
    GrowthModelSorter filter and sort original targets.

    Main factors as follows:
    ----------------------
    - 息税前利润率EBITG、
    - 归属母公司净利润增长率NPG、
    - 营业总收入增长率TAG、
    - 营业毛利润GPG、
    - 营业利润率OPG、
    - 每股现金流量净额OCG
    Sort by:
    ----------------------
    - weight score of all factors

    """

    def __init__(self):
        super().__init__()

    def sort(self, in_list: list) -> list:
        symbol_list = list(in_list)
        last_day = get_previous_trading_date("SHSE", self.now)
        day_time = last_day
        df = pd.DataFrame([])
        df["symbol"] = symbol_list
        df["EBITG"] = -999.0
        df["NPG"] = -999.0
        df["TAG"] = -999.0  # MPG取不到，用TAG代替
        df["GPG"] = -999.0
        df["OPG"] = -999.0
        df["OCG"] = -999.0
        # 求出 息税前利润率EBITG
        for number in range(len(symbol_list)):
            try:
                _df = get_fundamentals_n(table='deriv_finance_indicator', symbols=symbol_list[number],
                                         end_date=day_time,
                                         count=2, fields="EBITMARGIN")

                now_EBITMARGIN = _df[0]["EBITMARGIN"]
                last_EBITMARGIN = _df[1]["EBITMARGIN"]
                EBITG = ((now_EBITMARGIN - last_EBITMARGIN) / last_EBITMARGIN)

                df.iloc[number, 1] = EBITG
            except:
                df.iloc[number, 1] = -999

        # 求 归属母公司净利润增长率NPG
        _df = get_fundamentals(table='deriv_finance_indicator', symbols=symbol_list, start_date=day_time,
                               end_date=day_time,
                               fields="NPGRT", df=True)
        if len(_df) == len(symbol_list):
            df["NPG"] = _df["NPGRT"]
        else:
            for number in range(len(symbol_list)):
                try:
                    _df = get_fundamentals(table='deriv_finance_indicator', symbols=symbol_list[number],
                                           start_date=day_time,
                                           end_date=day_time, fields="NPGRT")
                    _NPG = get_data_value(_df, "NPGRT")

                    df.iloc[number, 2] = _NPG[0]
                except:
                    df.iloc[number, 2] = -999
        # 求出 营业总收入增长率TAG
        _df = get_fundamentals(table='deriv_finance_indicator', symbols=symbol_list, start_date=day_time,
                               end_date=day_time,
                               fields="TAGRT", df=True)
        if len(_df) == len(symbol_list):
            df["TAG"] = _df["TAGRT"]
        else:
            for number in range(len(symbol_list)):
                try:
                    _df = get_fundamentals(table='deriv_finance_indicator', symbols=symbol_list[number],
                                           start_date=day_time,
                                           end_date=day_time, fields="TAGRT")
                    _TAG = get_data_value(_df, "TAGRT")

                    df.iloc[number, 3] = _TAG[0]
                except:
                    df.iloc[number, 3] = -999

        # 求 营业毛利润GPG
        for number in range(len(symbol_list)):
            try:
                _df = get_fundamentals_n(table='deriv_finance_indicator', symbols=symbol_list[number],
                                         end_date=day_time,
                                         count=2, fields="OPGPMARGIN")

                now_GPG = _df[0]["OPGPMARGIN"]
                last_GPG = _df[1]["OPGPMARGIN"]
                GPG = ((now_GPG - last_GPG) / last_GPG)

                df.iloc[number, 4] = GPG
            except:
                df.iloc[number, 4] = -999

        # 求 营业利润率OPG
        for number in range(len(symbol_list)):
            try:
                _df = get_fundamentals_n(table='deriv_finance_indicator', symbols=symbol_list[number],
                                         end_date=day_time,
                                         count=2, fields="OPPRORT")

                now_OPG = _df[0]["OPPRORT"]
                last_OPG = _df[1]["OPPRORT"]
                OPG = ((now_OPG - last_OPG) / last_OPG)
                df.iloc[number, 5] = OPG
            except:
                df.iloc[number, 5] = -999
        # 求 每股现金流量净额OCG
        for number in range(len(symbol_list)):
            try:
                _df = get_fundamentals_n(table='deriv_finance_indicator', symbols=symbol_list[number],
                                         end_date=day_time,
                                         count=2, fields="NCFPS")
                now_EBITMARGIN = _df[0]["NCFPS"]
                last_EBITMARGIN = _df[1]["NCFPS"]
                EBITG = ((now_EBITMARGIN - last_EBITMARGIN) / last_EBITMARGIN)
                df.iloc[number, 6] = EBITG
            except:
                df.iloc[number, 6] = -999

        df = df.dropna()
        df_factor = df.iloc[:, 1:]
        df_factor = np.asarray(df_factor)

        # 先进行列归一化，然后在对每行进行标准化处理
        df_factor = preprocessing.MinMaxScaler().fit_transform(df_factor)
        weight = [[-1], [-1], [-1], [-1], [-1], [-1]]
        weight_mat = np.asmatrix(weight)
        res = np.dot(df_factor, weight_mat)
        df["score"] = (res)

        df = (df.sort_values(["score"]))
        # print(df)
        symbol_list = []
        for _ in df["symbol"].values:
            symbol_list.append(_)

        return symbol_list


