# -*- coding: utf-8 -*-
import time
import os
from gm.api import *

from sq import *

"""
sq test
Main Features
-------------
- group layer

"""


def init(context):
    context.start_time = time.time()
    print_log("Start...")
    context.num = 8
    context.symbol = "test_model_11_12"
    context.model = test_model_11_12(context)
    schedule(schedule_func=algo, date_rule='1d', time_rule='09:31:00')


def test_model_11_12(context):
    model1 = GMModel()
    # model1.add(AllSymbolSelector(list(index_list.keys())))
    # model1.add(BlackFilter())
    # model1.add(WhiteFilter([]))
    model1.add(PairTradeSorter("SHSE.601939", "SHSE.601288"))
    # model1.add(TopNFilter(context.num))
    model1.add(GMOrder(context.num))
    # 1.For SHSE.601939 & SHSE.601288, by month, 20140401~20240401, pnl_ratio  5.7%
    # every executing spend about 0.15 seconds. And from 2014-04-01 to 2024-04-01, it spends about 23 seconds.
    # test_model_11_12 backtest finished:
    #           {'account_id': '9f53e15f-6870-11e8-801c-4cedfb681747', 'pnl_ratio': 0.05785088703809452,
    #            'pnl_ratio_annual': 0.005778755820718254, 'sharp_ratio': 0.29601460201571744,
    #            'max_drawdown': 0.03823282354261679, 'risk_ratio': 0.12020717993657389, 'open_count': 88,
    #            'close_count': 87, 'win_count': 50, 'lose_count': 37, 'win_ratio': 0.5747126436781609,
    #            'calmar_ratio': 0.15114645702996216, 'created_at': None, 'updated_at': None}
    # 2.For SHSE.601939 & SHSE.601288, by week, 20140401~20240401, pnl_ratio  10.1%
    # every executing spend about 0.18 seconds. And from 2014-04-01 to 2024-04-01, it spends about 90 seconds.
    # test_model_11_12 backtest finished:
    #           {'account_id': '9f53e15f-6870-11e8-801c-4cedfb681747', 'pnl_ratio': 0.1015042928977881,
    #            'pnl_ratio_annual': 0.01013931770872815, 'sharp_ratio': 0.5004809175818425,
    #            'max_drawdown': 0.03682713467476974, 'risk_ratio': 0.12382620634771385, 'open_count': 363,
    #            'close_count': 362, 'win_count': 179, 'lose_count': 183, 'win_ratio': 0.494475138121547,
    #            'calmar_ratio': 0.2753219276566361, 'created_at': None, 'updated_at': None}
    # 3.For SHSE.601939 & SHSE.601288, by day, 20140401~20240401, pnl_ratio  13.8%
    # every executing spend about 0.18 seconds. And from 2014-04-01 to 2024-04-01, it spends about 455 seconds.
    # test_model_11_12 backtest finished:
    #           {'account_id': '9f53e15f-6870-11e8-801c-4cedfb681747', 'pnl_ratio': 0.13812647015452384,
    #            'pnl_ratio_annual': 0.013797526438533443, 'sharp_ratio': 0.6347147440499051,
    #            'max_drawdown': 0.03755642722249355, 'risk_ratio': 0.12493760938824412, 'open_count': 1737,
    #            'close_count': 1736, 'win_count': 725, 'lose_count': 1011, 'win_ratio': 0.4176267281105991,
    #            'calmar_ratio': 0.36738123029630826, 'created_at': None, 'updated_at': None}

    return model1


def algo(context):
    print_log(context.now, " algo...")
    context.model.execute(context.now)


def on_backtest_finished(context, indicator):
    print_log(f"Done! From start, time elapsed: {time.time() - context.start_time} seconds")
    print_log(f"{context.symbol} backtest finished: ", indicator)


if __name__ == "__main__":
    run(
        strategy_id='9f53e15f-6870-11e8-801c-4cedfb681747',
        filename=(os.path.basename(__file__)),
        mode=MODE_BACKTEST,
        token='42c5e7778813e4a38aae2e65d70eb372ac8f2435',
        backtest_start_time="2014-08-01 09:30:00",
        backtest_end_time='2024-08-01 15:00:00',
        backtest_initial_cash=10000000,
        backtest_adjust=ADJUST_PREV,
    )
