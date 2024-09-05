# -*- coding: utf-8 -*-
import time
import os
import pandas as pd
from gm.api import *
from pycallgraph2 import PyCallGraph
from pycallgraph2.output import GraphvizOutput
from sq import *
from sq.gm import get_time_Ymd

"""
sq test2
Main Features
-------------
- trainer

"""


def init(context):
    context.start_time = time.time()
    print_log("Start...")
    context.num = 8
    context.symbol = "SHSE.000922"
    context.model = init_model_13_1(context)
    schedule(schedule_func=algo, date_rule='1d', time_rule='10:31:00')
    # context.all_date = []


def init_model_9_7(context):
    model1 = GMModel()
    # model1.add(AllSymbolSelector(list(index_list.keys())))
    # model1.add(BlackFilter())
    model1.add(WhiteFilter([context.symbol]))
    # model1.add(TopNFilter(context.num))
    model1.add(SVMOrder(context, model1))
    model1.add_trainer(SVMTrainer(context.symbol, "2014-01-01", "2024-01-01"))
    model1.train()
    # 1.For SHSE.000922, by day, 20140801~20240801, pnl_ratio  53.9%.  train period 2016-01-01~2020-01-01
    # every executing spend about 0.1 seconds. And from 2014-08-01 to 2024-08-01, it spends about 241 seconds.
    # init_model_9_7 backtest finished:
    #           {'account_id': '16362727-4aff-11ef-8fae-80304917db79', 'pnl_ratio': 0.5393140445457272,
    #            'pnl_ratio_annual': 0.053872366244989166, 'sharp_ratio': 0.17336764427392254,
    #            'max_drawdown': 0.37594106676401623, 'risk_ratio': 0.948981711243112, 'open_count': 434,
    #            'close_count': 433, 'win_count': 232, 'lose_count': 201, 'win_ratio': 0.535796766743649,
    #            'calmar_ratio': 0.143300030264599, 'created_at': None, 'updated_at': None}
    # 2.For SHSE.000922, by day, 20140801~20240801, pnl_ratio  53.9%.  train period 2014-01-01~2024-01-01
    # every executing spend about 0.1 seconds. And from 2014-08-01 to 2024-08-01, it spends about 260 seconds.
    # init_model_9_7 backtest finished:
    #           {'account_id': '16362727-4aff-11ef-8fae-80304917db79', 'pnl_ratio': 0.5393140445457272,
    #            'pnl_ratio_annual': 0.053872366244989166, 'sharp_ratio': 0.17336764427392254,
    #            'max_drawdown': 0.37594106676401623, 'risk_ratio': 0.948981711243112, 'open_count': 434,
    #            'close_count': 433, 'win_count': 232, 'lose_count': 201, 'win_ratio': 0.535796766743649,
    #            'calmar_ratio': 0.143300030264599, 'created_at': None, 'updated_at': None}

    return model1


def init_model_13_1(context):
    model1 = GMModel()
    # model1.add(AllSymbolSelector(list(index_list.keys())))
    # model1.add(BlackFilter())
    model1.add(WhiteFilter([context.symbol]))
    # model1.add(TopNFilter(context.num))
    model1.add(ManualOrder(context, model1))
    model1.add_trainer(ManualTrainer(context.symbol, model_index=1))
    model1.train()
    # backtest result of model_index = 0~7: see sq_test3_1_backtest.md
    return model1


def algo(context):
    print_log(context.now, " algo...")
    context.model.execute(context.now)


def on_backtest_finished(context, indicator):
    print_log(f"Done! From start, time elapsed: {time.time() - context.start_time} seconds")
    print_log(f"{context.symbol} backtest finished: ", indicator)


if __name__ == "__main__":
    '''
        strategy_id策略ID, 由系统生成
        filename文件名, 请与本文件名保持一致
        mode运行模式, 实时模式:MODE_LIVE回测模式:MODE_BACKTEST
        token绑定计算机的ID, 可在系统设置-密钥管理中生成
        backtest_start_time回测开始时间
        backtest_end_time回测结束时间
        backtest_adjust股票复权方式, 不复权:ADJUST_NONE前复权:ADJUST_PREV后复权:ADJUST_POST
        backtest_initial_cash回测初始资金
        backtest_commission_ratio回测佣金比例
        backtest_slippage_ratio回测滑点比例
        backtest_match_mode市价撮合模式，以下一tick/bar开盘价撮合:0，以当前tick/bar收盘价撮合：1
        '''
    run(
        strategy_id='16362727-4aff-11ef-8fae-80304917db79',
        filename=(os.path.basename(__file__)),
        mode=MODE_BACKTEST,
        token='42c5e7778813e4a38aae2e65d70eb372ac8f2435',
        backtest_start_time="2008-11-01 09:30:00",
        backtest_end_time='2024-08-30 15:00:00',
        backtest_initial_cash=10000000,
        backtest_adjust=ADJUST_PREV,
        backtest_slippage_ratio=0.00000,
        backtest_commission_ratio=0.00000,
    )
