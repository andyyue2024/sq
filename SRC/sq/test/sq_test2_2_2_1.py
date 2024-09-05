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
    context.symbol = "test_model_9_4"
    context.model = test_model_9_4(context)
    schedule(schedule_func=algo, date_rule='1d', time_rule='09:31:00')


def test_model_5_9(context):
    model1 = GMModel()
    # model1.add(AllSymbolSelector(list(index_list.keys())))
    # model1.add(BlackFilter())
    # model1.add(WhiteFilter())
    # model1.add(TopNFilter(context.num))
    model1.add(SingleFactor1Order("SZSE.300296"))
    # 1.For SHSE.300296, by day, 20140401~20240401, pnl_ratio  -58%
    # every executing spend about 0.08 seconds. And from 2014-08-01 to 2024-08-01, it spends about 225 seconds.
    # test_model_5_9 backtest finished:
    #           {'account_id': '9f53e15f-6870-11e8-801c-4cedfb681747', 'pnl_ratio': -0.5818418979644775,
    #            'pnl_ratio_annual': -0.058120496102089296, 'sharp_ratio': -0.20335274708229714,
    #            'max_drawdown': 0.7032235378317147, 'open_count': 44, 'close_count': 41, 'win_count': 13,
    #            'lose_count': 28, 'win_ratio': 0.3170731707317073, 'calmar_ratio': -0.08264867851450935,
    #            'risk_ratio': 0.0, 'created_at': None, 'updated_at': None}

    return model1


def test_model_5_10(context):
    model1 = GMModel()
    # model1.add(AllSymbolSelector(list(index_list.keys())))
    # model1.add(BlackFilter())
    # model1.add(WhiteFilter())
    # model1.add(TopNFilter(context.num))
    model1.add(SingleFactor2Order("SZSE.300296"))
    # 1.For SHSE.300296, by day, 20140401~20240401, pnl_ratio  42%
    # every executing spend about 0.08 seconds. And from 2014-08-01 to 2024-08-01, it spends about 238 seconds.
    # test_model_5_10 backtest finished:
    #           {'account_id': '9f53e15f-6870-11e8-801c-4cedfb681747', 'pnl_ratio': 0.4234665870666504,
    #            'pnl_ratio_annual': 0.04230030221109124, 'sharp_ratio': 0.12646899287467975,
    #            'max_drawdown': 0.5638533969649906, 'risk_ratio': 0.9952111811071993, 'open_count': 9, 'close_count': 8,
    #            'win_count': 6, 'lose_count': 2, 'win_ratio': 0.75, 'calmar_ratio': 0.07502003612779094,
    #            'created_at': None, 'updated_at': None}

    return model1


def test_model_5_12(context):
    model1 = GMModel()
    # model1.add(AllSymbolSelector(list(index_list.keys())))
    # model1.add(BlackFilter())
    # model1.add(WhiteFilter())
    # model1.add(TopNFilter(context.num))
    model1.add(SingleFactor3Order("SHSE.600000"))
    # 1.For SHSE.600000, by day, 20140401~20240401, pnl_ratio  79%
    # every executing spend about 0.2 seconds. And from 2014-08-01 to 2024-08-01, it spends about 468 seconds.
    # test_model_5_12 backtest finished:
    #           {'account_id': '9f53e15f-6870-11e8-801c-4cedfb681747', 'pnl_ratio': 0.7945122714042664,
    #            'pnl_ratio_annual': 0.07936425261701074, 'sharp_ratio': 0.2000131829938173,
    #            'max_drawdown': 0.41147126705355164, 'risk_ratio': 1.0027235114757578, 'open_count': 1,
    #            'calmar_ratio': 0.19287920924666108, 'close_count': 0, 'win_count': 0, 'lose_count': 0, 'win_ratio': 0.0,
    #            'created_at': None, 'updated_at': None}

    return model1


def test_model_7_1(context):
    model1 = GMModel()
    # model1.add(AllSymbolSelector(list(index_list.keys())))
    # model1.add(BlackFilter())
    # model1.add(WhiteFilter())
    # model1.add(TopNFilter(context.num))
    model1.add(SingleFactor4Order("SHSE.000300"))
    # 1.For SHSE.000300, by day, 20140401~20240401, pnl_ratio  9.6%
    # every executing spend about 0.1 seconds. And from 2014-08-01 to 2024-08-01, it spends about 273 seconds.
    # test_model_7_1 backtest finished:
    #           {'account_id': '9f53e15f-6870-11e8-801c-4cedfb681747', 'pnl_ratio': 0.09663699951171875,
    #            'pnl_ratio_annual': 0.009653121188225875, 'sharp_ratio': 0.04777968596679928,
    #            'max_drawdown': 0.5026843863282578, 'risk_ratio': 0.9991811947825168, 'open_count': 46,
    #            'close_count': 45, 'win_count': 20, 'lose_count': 25, 'win_ratio': 0.4444444444444444,
    #            'calmar_ratio': 0.01920314505635409, 'created_at': None, 'updated_at': None}

    return model1


def test_model_7_3(context):
    model1 = GMModel()
    # model1.add(AllSymbolSelector(list(index_list.keys())))
    # model1.add(BlackFilter())
    # model1.add(WhiteFilter())
    # model1.add(TopNFilter(context.num))
    model1.add(SingleFactor5Order("SHSE.000300"))
    # 1.For SHSE.000300, by day, 20140801~20240801, pnl_ratio  25%
    # every executing spend about 0.4 seconds. And from 2014-08-01 to 2024-08-01, it spends about 1022 seconds.
    # test_model_7_3 backtest finished:
    #           {'account_id': '9f53e15f-6870-11e8-801c-4cedfb681747', 'pnl_ratio': 0.2544775209960938,
    #            'pnl_ratio_annual': 0.025419894680781124, 'sharp_ratio': 0.1093026380251164,
    #            'max_drawdown': 0.42296087399688914, 'risk_ratio': 1.0000764201243066, 'open_count': 38,
    #            'close_count': 37, 'win_count': 14, 'lose_count': 23, 'win_ratio': 0.3783783783783784,
    #            'calmar_ratio': 0.06009987269169509, 'created_at': None, 'updated_at': None}

    return model1

def test_model_9_4(context):
    model1 = GMModel()
    # model1.add(AllSymbolSelector(list(index_list.keys())))
    # model1.add(BlackFilter())
    # model1.add(WhiteFilter())
    # model1.add(TopNFilter(context.num))
    model1.add(SingleFactor6Order("SHSE.601318"))
    # 1.For SHSE.601318, by day, 20140801~20240801, pnl_ratio  166%
    # every executing spend about 0.18 seconds. And from 2014-08-01 to 2024-08-01, it spends about 481 seconds.
    # test_model_9_4 backtest finished:
    #           {'account_id': '9f53e15f-6870-11e8-801c-4cedfb681747', 'pnl_ratio': 1.6617308438682556,
    #            'pnl_ratio_annual': 0.16599117624847107, 'sharp_ratio': 0.2898214895627856,
    #            'max_drawdown': 0.45956087719428446, 'risk_ratio': 1.0016340382492321, 'open_count': 391,
    #            'close_count': 389, 'win_count': 196, 'lose_count': 193, 'win_ratio': 0.5038560411311054,
    #            'calmar_ratio': 0.36119518541674395, 'created_at': None, 'updated_at': None}

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
