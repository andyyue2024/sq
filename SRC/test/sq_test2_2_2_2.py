# -*- coding: utf-8 -*-
import time
import os
from gm.api import *
from sq import *

"""
sq test
Main Features
-------------
- layer
"""


def init(context):
    context.start_time = time.time()
    print_log("Start...")
    context.num = 8
    context.symbol = "test_model_5_13"
    context.model = test_model_5_13(context)
    schedule(schedule_func=algo, date_rule='1d', time_rule='09:31:00')


def test_model_5_13(context):
    model1 = GMModel()
    # model1.add(AllSymbolSelector(list(index_list.keys())))
    # model1.add(BlackFilter())
    # model1.add(WhiteFilter())
    # model1.add(TopNFilter(context.num))
    model1.add(MultiFactors1Order("SHSE.600000"))
    # 1.For SHSE.600000, by day, 20140801~20240801, pnl_ratio  5.2%
    # every executing spend about 0.18 seconds. And from 2014-08-01 to 2024-08-01, it spends about 470 seconds.
    # test_model_5_13 backtest finished:
    #           {'account_id': '16362727-4aff-11ef-8fae-80304917db79', 'pnl_ratio': 0.052164104919433595,
    #            'pnl_ratio_annual': 0.00521070013563034, 'sharp_ratio': 0.02416750066811101,
    #            'max_drawdown': 0.39147492551578694, 'risk_ratio': 1.0183557843650453, 'open_count': 4, 'close_count': 3,
    #            'win_count': 2, 'lose_count': 1, 'win_ratio': 0.6666666666666666, 'calmar_ratio': 0.01331043138654409,
    #            'created_at': None, 'updated_at': None}

    return model1


def algo(context):
    print_log(context.now, " algo...")
    context.model.execute(context.now)


def on_backtest_finished(context, indicator):
    print_log(f"Done! From start, time elapsed: {time.time() - context.start_time} seconds")
    print_log(f"{context.symbol} backtest finished: ", indicator)

if __name__ == "__main__":
    run(
        strategy_id='16362727-4aff-11ef-8fae-80304917db79',
        filename=(os.path.basename(__file__)),
        mode=MODE_BACKTEST,
        token='42c5e7778813e4a38aae2e65d70eb372ac8f2435',
        backtest_start_time="2014-08-01 09:30:00",
        backtest_end_time='2024-08-01 15:00:00',
        backtest_initial_cash=10000000,
        backtest_adjust=ADJUST_PREV,
    )
