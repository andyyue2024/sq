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
    context.num = 5
    context.title = "test_model_7_4"
    context.model = test_model_7_4(context)
    schedule(schedule_func=algo, date_rule='1m', time_rule='09:31:00')


def test_model_6_6(context):
    model1 = GMModel()
    model1.add(AllSymbolSelector(["SHSE.000010"]))
    # model1.add(BlackFilter([], ["SHSE.000947", "SZSE.399975"]))
    # model1.add(WhiteFilter(["SHSE.600519", "SZSE.300896"]))
    model1.add(HowardRothmanSorter())
    model1.add(TopNFilter(context.num))
    model1.add(GMOrder(context.num))

    # 1.For SHSE.000016, top 5 , 20140401~20240401, pnl_ratio 91%
    # every executing spend about 1.4 seconds. And from 2014-04-01 to 2024-04-01, it spends about 153 seconds.
    # test_model_6_6 backtest finished:
    #           {'account_id': '9f53e15f-6870-11e8-801c-4cedfb681747', 'pnl_ratio': 0.9138821334922314,
    #            'pnl_ratio_annual': 0.09128817151742322, 'sharp_ratio': 0.2332772009010014,
    #            'max_drawdown': 0.5280780787922809, 'risk_ratio': 0.5952063758306132, 'open_count': 441,
    #            'close_count': 438, 'win_count': 238, 'lose_count': 200, 'win_ratio': 0.54337899543379,
    #            'calmar_ratio': 0.17286870101898577, 'created_at': None, 'updated_at': None}

    # 2.For SHSE.000010, top 5 , 20140401~20240401, pnl_ratio 138%
    # every executing spend about 1.7 seconds. And from 2014-04-01 to 2024-04-01, it spends about 223 seconds.
    # test_model_6_6 backtest finished:
    #           {'account_id': '9f53e15f-6870-11e8-801c-4cedfb681747', 'pnl_ratio': 1.3821828059113026,
    #            'pnl_ratio_annual': 0.13806697431790516, 'sharp_ratio': 0.18274216950386832,
    #            'max_drawdown': 0.5805458570707155, 'risk_ratio': 0.9964616755231496, 'open_count': 552,
    #            'close_count': 547, 'win_count': 279, 'lose_count': 268, 'win_ratio': 0.5100548446069469,
    #            'calmar_ratio': 0.2378226846963571, 'created_at': None, 'updated_at': None}

    return model1


def test_model_6_7(context):
    model1 = GMModel()
    model1.add(AllSymbolSelector(["SHSE.000010"]))
    # model1.add(BlackFilter([], ["SHSE.000947", "SZSE.399975"]))
    # model1.add(WhiteFilter(["SHSE.600519", "SZSE.300896"]))
    model1.add(GrowthModelSorter())
    model1.add(TopNFilter(context.num))
    model1.add(GMOrder(context.num))
    return model1


def test_model_7_4(context):
    model1 = GMModel()
    model1.add(AllSymbolSelector(["SHSE.000922"]))
    # model1.add(BlackFilter([], ["SHSE.000947", "SZSE.399975"]))
    # model1.add(WhiteFilter(["SHSE.600519", "SZSE.300896"]))
    # model1.add(TopNFilter(context.num))
    model1.add(VIPAOrder(context))
    # 1.For SHSE.000922, top 10 , by month, 20140401~20240401, pnl_ratio 41%
    # every executing spend about 12 seconds. And from 2014-04-01 to 2024-04-01, it spends about 153 seconds.
    # test_model_7_4 backtest finished:
    #           {'account_id': '16362727-4aff-11ef-8fae-80304917db79', 'pnl_ratio': 0.4159365182185173,
    #            'pnl_ratio_annual': 0.04154811963594932, 'sharp_ratio': 0.3915356015543102,
    #            'max_drawdown': 0.3045970278384549, 'risk_ratio': 0.5072076450494366, 'open_count': 8, 'close_count': 2,
    #            'win_count': 2, 'win_ratio': 1.0, 'calmar_ratio': 0.1364035622106748, 'lose_count': 0,
    #            'created_at': None, 'updated_at': None}

    return model1



def test_model_8_1(context):
    model1 = GMModel()
    model1.add(AllSymbolSelector(["SHSE.000922"]))
    # model1.add(BlackFilter([], ["SHSE.000947", "SZSE.399975"]))
    # model1.add(WhiteFilter(["SHSE.600519", "SZSE.300896"]))
    model1.add(DefensiveStrategySorter())
    model1.add(TopNFilter(context.num))
    model1.add(GMOrder(context.num))
    # 1.For SHSE.000922, top 5 , 20140401~20240401, pnl_ratio  %
    # every executing spend about 37 seconds. And from 2014-04-01 to 2024-04-01, it spends about 153 seconds.
    # test_model_8_1 backtest finished:
    return model1


def test_model_8_2(context):
    factor_dict = {
        "PETTM": "PETTM > 0",  # 市盈率TTM
        "ROEAVGCUT": "",  # 净资产收益率_平均(扣除非经常损益)
        "DY": "",  # 股息率(滚动12月-按证监会口径)
        "PB": "",  # 市净率(PB)
        "ROIC": "",  # 投入资本回报率
    }
    weight = [1, -1, -1, 1, -1]
    model1 = GMModel()
    model1.add(AllSymbolSelector(["SHSE.000922"]))
    # model1.add(BlackFilter([], ["SHSE.000947", "SZSE.399975"]))
    # model1.add(WhiteFilter(["SHSE.600519", "SZSE.300896"]))
    model1.add(MultiFactors3Sorter(factor_dict, weight))
    model1.add(TopNFilter(context.num))
    model1.add(GMOrder(context.num))
    # 1.For SHSE.000922, top 5 , 20140401~20240401, pnl_ratio  %
    # every executing spend about 37 seconds. And from 2014-04-01 to 2024-04-01, it spends about 153 seconds.
    # test_model_8_2 backtest finished:
    return model1


def test_model_10_1(context):
    model1 = GMModel()
    model1.add(AllSymbolSelector(["SHSE.000300"]))
    # model1.add(BlackFilter([], ["SHSE.000947", "SZSE.399975"]))
    # model1.add(WhiteFilter(["SHSE.600519", "SZSE.300896"]))
    model1.add(FamaFrenchSorter())
    # model1.add(TopNFilter(context.num))
    model1.add(AverageOrder())
    # 1.For SHSE.000300, average order filtered target,  20140401~20240401, pnl_ratio  28%
    # every executing spend about 38 seconds. And from 2014-04-01 to 2024-04-01, it spends about 4613 seconds.
    # test_model_10_1 backtest finished:
    #           {'account_id': '16362727-4aff-11ef-8fae-80304917db79', 'pnl_ratio': 0.283894640519619,
    #            'pnl_ratio_annual': 0.028358386368270646, 'sharp_ratio': 0.060018483250051984,
    #            'max_drawdown': 0.7024353340344198, 'risk_ratio': 1.0101177380634354, 'open_count': 1159,
    #            'close_count': 1149, 'win_count': 549, 'lose_count': 600, 'win_ratio': 0.47780678851174935,
    #            'calmar_ratio': 0.04037152602417501, 'created_at': None, 'updated_at': None}

    return model1


def algo(context):
    print_log(context.now, " algo...")
    context.model.execute(context.now)


def on_backtest_finished(context, indicator):
    print_log(f"Done! From start, time elapsed: {time.time() - context.start_time} seconds")
    print_log(f"{context.title} backtest finished: ", indicator)


if __name__ == "__main__":
    run(
        strategy_id='16362727-4aff-11ef-8fae-80304917db79',
        filename=(os.path.basename(__file__)),
        mode=MODE_BACKTEST,
        token='42c5e7778813e4a38aae2e65d70eb372ac8f2435',
        backtest_start_time="2014-04-01 09:30:00",
        backtest_end_time='2024-04-01 15:00:00',
        backtest_initial_cash=10000000,
        backtest_adjust=ADJUST_PREV,
    )
