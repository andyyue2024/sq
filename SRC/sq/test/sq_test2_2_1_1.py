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
    context.title = "test_model_10_5"
    context.model = test_model_10_5(context)
    schedule(schedule_func=algo, date_rule='1m', time_rule='10:31:00')


def test_model_10_3(context):
    model1 = GMModel()
    model1.add(AllSymbolSelector(list(index_list.keys())))
    model1.add(BlackFilter([], []))
    model1.add(WhiteFilter(["SHSE.600519", "SZSE.300896"]))
    model1.add(MultiFactors1Sorter())
    model1.add(TopNFilter(context.num))
    model1.add(GMOrder(context.num))
    model1.execute(context.now)
    # every executing spend about 320 seconds. And from 2014-08-01 to 2016-08-01, it spends about 7687 seconds.
    # test_model_10_3 backtest finished: {'account_id': '9f53e15f-6870-11e8-801c-4cedfb681747', 'pnl_ratio':
    # -0.011146216171048145, 'pnl_ratio_annual': -0.005557881014252149, 'sharp_ratio': -0.01282056183975542,
    # 'max_drawdown': 0.4268787780266562, 'risk_ratio': 0.960617870258613, 'open_count': 208, 'close_count': 200,
    # 'win_count': 90, 'lose_count': 110, 'win_ratio': 0.45, 'calmar_ratio': -0.013019811010387333, 'created_at':
    # None, 'updated_at': None}

    return model1


def test_model_10_5(context):
    model1 = GMModel()
    model1.add(AllSymbolSelector(list(index_list.keys())))
    model1.add(MultiFactorsPBROESorter())
    # model1.add(MultiFactors2Sorter({"PB": "PB > 0", "ROEAVG": "ROEAVG > 0"}))
    model1.add(TopNFilter(context.num))
    model1.add(GMOrder(context.num))
    model1.execute(context.now)
    # 1.For SHSE.000922
    # every executing spend about 6 seconds. And from 2014-08-01 to 2016-08-01, it spends about 144 seconds.
    # test_model_10_5 backtest finished:
    #           {'account_id': '9f53e15f-6870-11e8-801c-4cedfb681747', 'pnl_ratio': 0.14794348182669856,
    #            'pnl_ratio_annual': 0.07376963233161882, 'sharp_ratio': 0.12130426667386826,
    #            'max_drawdown': 0.46870512507180195, 'risk_ratio': 0.961896901389304, 'open_count': 205,
    #            'close_count': 197, 'win_count': 96, 'lose_count': 101, 'win_ratio': 0.4873096446700508,
    #            'calmar_ratio': 0.15739028311311484, 'created_at': None, 'updated_at': None}
    # 2.For index_list
    # every executing spend about 406 seconds. And from 2014-08-01 to 2016-08-01, it spends about 9765 seconds.
    # test_model_10_5 backtest finished:
    #           {'account_id': '9f53e15f-6870-11e8-801c-4cedfb681747', 'pnl_ratio': 0.20684674889018148,
    #            'pnl_ratio_annual': 0.10314079691928447, 'sharp_ratio': 0.1533165355113877,
    #            'max_drawdown': 0.584965982181971, 'risk_ratio': 0.9698340294049254, 'open_count': 207,
    #            'close_count': 199, 'win_count': 103, 'lose_count': 96, 'win_ratio': 0.5175879396984925,
    #            'calmar_ratio': 0.1763193075511175, 'created_at': None, 'updated_at': None}
    return model1


def algo(context):
    print_log(context.now, " algo...")
    context.model.execute(context.now)


def on_backtest_finished(context, indicator):
    print_log(f"Done! From start, time elapsed: {time.time() - context.start_time} seconds")
    print_log(f"{context.title} backtest finished: ", indicator)


index_list = {
    # SHSE
    "SHSE.000001": "上证指数",
    "SHSE.000002": "A股指数",
    "SHSE.000004": "工业指数",
    "SHSE.000005": "商业指数",
    "SHSE.000006": "地产指数",
    "SHSE.000007": "公用指数",
    "SHSE.000008": "综合指数",
    "SHSE.000009": "上证380",
    "SHSE.000010": "上证180",
    "SHSE.000015": "红利指数",
    "SHSE.000016": "上证50",
    "SHSE.000017": "新综指",
    "SHSE.000018": "180金融",
    "SHSE.000300": "沪深300",
    "SHSE 000903": "中证100",
    "SHSE.000904": "中证200",
    "SHSE.000905": "中证500",
    "SHSE.000906": "中证800",
    "SHSE.000907": "中证700",
    "SHSE.000922": "中证红利",
    "SHSE.000852": "中证1000",
    # SZSE
    "SZSE.399001": "深证成指",
    "SZSE.399002": "深成指R",
    "SZSE.399004": "深证100R",
    "SZSE.399005": "中小板指",
    "SZSE.399006": "中小板指",
    "SZSE.399007": "深证300",
    "SZSE.399008": "中小300",
    "SZSE.399009": "深证200",
    "SZSE.399010": "深证700",
    "SZSE.399011": "深证1000",
    "SZSE.399012": "创业300",
}

if __name__ == "__main__":
    run(
        strategy_id='9f53e15f-6870-11e8-801c-4cedfb681747',
        filename=(os.path.basename(__file__)),
        mode=MODE_BACKTEST,
        token='42c5e7778813e4a38aae2e65d70eb372ac8f2435',
        backtest_start_time="2014-08-01 09:30:00",
        backtest_end_time='2016-08-01 15:00:00',
        backtest_initial_cash=100000,
        backtest_adjust=ADJUST_PREV,
        backtest_slippage_ratio=0.01,
        backtest_commission_ratio=0.0005,
    )
