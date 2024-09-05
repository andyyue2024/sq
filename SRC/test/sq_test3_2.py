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
sq test3
Main Features
-------------
- group trainer

"""


def init(context):
    context.start_time = time.time()
    print_log("Start...")
    # context.num = 8
    context.symbol = "SHSE.000922"
    context.model = init_model_13_2(context)
    schedule(schedule_func=algo, date_rule='1d', time_rule='10:31:00')


def init_model_13_2(context):
    model1 = GMModel()
    # model1.add(AllSymbolSelector(list(index_list.keys())))
    # model1.add(BlackFilter())
    model1.add(WhiteFilter([context.symbol]))
    # model1.add(TopNFilter(context.num))
    model1.add(ManualOrder(context, model1))
    model1.add_trainer(ManualTrainer(context.symbol, start_date="2004-08-01",
                                     end_date="2024-08-30", model_index=4, fast_prediction=True))
    model1.add_trainer(ManualTrainer(context.symbol, start_date="2004-08-01",
                                     end_date="2024-08-30", model_index=6, fast_prediction=True))
    # model1.add_trainer(ManualTrainer(context.symbol, model_index=4))
    # model1.add_trainer(ManualTrainer(context.symbol, model_index=6))
    model1.train()
    # 1.For SHSE.000922, by day, 20081101~20240830, pnl_ratio 2813667.58%.
    # every executing spend about 0.0 seconds. And during period, it spends about (83-75) seconds.
    # model index 4: StackedEnsemble_BestOfFamily_1_AutoML_1_20240830_224552
    # model index 6: StackedEnsemble_BestOfFamily_1_AutoML_2_20240831_100856
    # init_model_13_2 backtest finished:
    #           {'account_id': '16362727-4aff-11ef-8fae-80304917db79', 'pnl_ratio': 28136.67585992561,
    #            'pnl_ratio_annual': 1776.7970049953024, 'sharp_ratio': 2.4613662874854145,
    #            'max_drawdown': 0.14057980045232765, 'open_count': 180, 'close_count': 180,
    #            'win_count': 178, 'lose_count': 2, 'win_ratio': 0.9888888888888889,
    #            'calmar_ratio': 12639.06335958868, 'risk_ratio': 0.0}

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
