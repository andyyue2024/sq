from sq.gm.tools import *
from sq.layers import Sorter


class FamaFrenchSorter(Sorter):
    """
    FamaFrenchSorter filter and sort original targets.

    Main factors as follows:
    ----------------------
    - NEGOTIABLEMV
    - PB
    - sort by alpha

    """
    # 数据滑窗
    context = {}
    DATA_WINDOW = 20
    # 设置开仓的最大资金量
    RATIO = 0.8
    # 账面市值比的大/中/小分类
    BM_BIG = 3.0
    BM_MID = 2.0
    BM_SMA = 1.0
    # 市值大/小分类
    MV_BIG = 2.0
    MV_SMA = 1.0

    def __init__(self):
        super().__init__()

    def sort(self, in_list: list) -> list:
        symbol_list = list(in_list)
        last_day = get_previous_trading_date(exchange='SHSE', date=self.now)
        fin = get_fundamentals_without_limit(table='tq_sk_finindic', symbols=symbol_list, start_date=last_day,
                                             end_date=last_day,
                                             fields='PB, NEGOTIABLEMV', df=True)
        # 计算账面市值比,为P/B的倒数
        fin['PB'] = (fin['PB'] ** -1)
        # 计算市值的50%的分位点,用于后面的分类
        size_gate = fin['NEGOTIABLEMV'].quantile(0.50)
        # 计算账面市值比的30%和70%分位点,用于后面的分类
        bm_gate = [fin['PB'].quantile(0.30), fin['PB'].quantile(0.70)]
        fin.index = fin.symbol
        x_return = []
        # 对未停牌的股票进行处理
        for symbol in symbol_list:
            # 计算收益率
            close = history_n(symbol=symbol, frequency='1d', count=FamaFrenchSorter.DATA_WINDOW + 1, end_time=last_day,
                              fields='close',
                              skip_suspended=True, fill_missing='Last', adjust=ADJUST_PREV, df=True)['close'].values
            stock_return = close[-1] / close[0] - 1
            pb = fin['PB'][symbol]
            market_value = fin['NEGOTIABLEMV'][symbol]
            # 获取[股票代码. 股票收益率, 账面市值比的分类, 市值的分类, 流通市值]
            if pb < bm_gate[0]:
                if market_value < size_gate:
                    label = [symbol, stock_return, FamaFrenchSorter.BM_SMA, FamaFrenchSorter.MV_SMA, market_value]
                else:
                    label = [symbol, stock_return, FamaFrenchSorter.BM_SMA, FamaFrenchSorter.MV_BIG, market_value]
            elif pb < bm_gate[1]:
                if market_value < size_gate:
                    label = [symbol, stock_return, FamaFrenchSorter.BM_MID, FamaFrenchSorter.MV_SMA, market_value]
                else:
                    label = [symbol, stock_return, FamaFrenchSorter.BM_MID, FamaFrenchSorter.MV_BIG, market_value]
            elif market_value < size_gate:
                label = [symbol, stock_return, FamaFrenchSorter.BM_BIG, FamaFrenchSorter.MV_SMA, market_value]
            else:
                label = [symbol, stock_return, FamaFrenchSorter.BM_BIG, FamaFrenchSorter.MV_BIG, market_value]
            if len(x_return) == 0:
                x_return = label
            else:
                x_return = np.vstack([x_return, label])
        stocks = pd.DataFrame(data=x_return, columns=['symbol', 'return', 'BM', 'NEGOTIABLEMV', 'mv'])
        stocks.index = stocks.symbol
        columns = ['return', 'BM', 'NEGOTIABLEMV', 'mv']
        for column in columns:
            stocks[column] = stocks[column].astype(np.float64)
        # 计算SMB.HML和市场收益率
        # 获取小市值组合的市值加权组合收益率
        smb_s = (market_value_weighted(stocks, FamaFrenchSorter.MV_SMA, FamaFrenchSorter.BM_SMA) +
                 market_value_weighted(stocks, FamaFrenchSorter.MV_SMA, FamaFrenchSorter.BM_MID) +
                 market_value_weighted(stocks, FamaFrenchSorter.MV_SMA, FamaFrenchSorter.BM_BIG)) / 3
        # 获取大市值组合的市值加权组合收益率
        smb_b = (market_value_weighted(stocks, FamaFrenchSorter.MV_BIG, FamaFrenchSorter.BM_SMA) +
                 market_value_weighted(stocks, FamaFrenchSorter.MV_BIG, FamaFrenchSorter.BM_MID) +
                 market_value_weighted(stocks, FamaFrenchSorter.MV_BIG, FamaFrenchSorter.BM_BIG)) / 3
        smb = smb_s - smb_b
        # 获取大账面市值比组合的市值加权组合收益率
        hml_b = (market_value_weighted(stocks, FamaFrenchSorter.MV_SMA, FamaFrenchSorter.BM_BIG) +
                 market_value_weighted(stocks, FamaFrenchSorter.MV_BIG, FamaFrenchSorter.BM_BIG)) / 2
        # 获取小账面市值比组合的市值加权组合收益率
        hml_s = (market_value_weighted(stocks, FamaFrenchSorter.MV_SMA, FamaFrenchSorter.BM_SMA) +
                 market_value_weighted(stocks, FamaFrenchSorter.MV_BIG, FamaFrenchSorter.BM_SMA)) / 2
        hml = hml_b - hml_s
        close = history_n(symbol='SHSE.000300', frequency='1d', count=FamaFrenchSorter.DATA_WINDOW + 1,
                          end_time=last_day, fields='close', skip_suspended=True,
                          fill_missing='Last', adjust=ADJUST_PREV, df=True)['close'].values
        market_return = close[-1] / close[0] - 1
        coff_pool = []
        # 对每只股票进行回归获取其alpha值
        for stock in stocks.index:
            x_value = np.array([[market_return], [smb], [hml], [1.0]])
            y_value = np.array([stocks['return'][stock]])
            # OLS估计系数
            coff = np.linalg.lstsq(x_value.T, y_value)[0][3]
            coff_pool.append(coff)
        # 获取alpha最小并且小于0的10只的股票进行操作(若少于10只则全部买入)
        stocks['alpha'] = coff_pool
        stocks = stocks[stocks.alpha < 0].sort_values(by='alpha').head(10)
        symbol_list = stocks.index.tolist()
        return symbol_list


