from sq.gm.tools import *
from sq.layers import Sorter


class MultiFactorsPBROESorter(Sorter):
    """
    MultiFactorsPBROESorter filter and sort original targets.

    Main factors as follows:
    ----------------------
    - PB, PB>0，
    - ROEAVG, ROEAVG>0
    - sort by delta value of ROE-PB OLS linear regression
    """

    def __init__(self):
        super().__init__()

    def sort(self, in_list: list) -> list:
        last_day = get_previous_trading_date("SHSE", self.now)
        symbol_list = list(in_list)
        factor_dict = {
            "ROEAVG": "ROEAVG > 0",
            "PB": "PB > 0",
            # "EBITMARGIN": "",
        }
        df = pd.DataFrame([])
        df["symbol"] = symbol_list
        df = get_fundamentals_without_limit3(symbols=symbol_list, start_date=last_day, end_date=last_day,
                                             fields_and_filter=factor_dict, df=True)
        df = df.rename(columns={'ROEAVG': 'ROE'})
        # Step 4: query to filter
        # df = df[(df['PB'] > 0) & (df['ROE'] > 0)]
        # df = df.query('PB > 2 and ROE > 0')
        df = df.dropna()
        symbol_list = get_symbol_list_by_delta_value(df, ["ROE"], "PB", "symbol")
        return symbol_list


