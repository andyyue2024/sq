# -*- coding: utf-8 -*-
import time

from gm.api import *
from pycallgraph2 import PyCallGraph
from pycallgraph2.output import GraphvizOutput

from sq import *

"""
sq test
Main Features
-------------
- model
- PyCallGraph and Graphviz

"""


def init(context):
    context.start_time = time.time()
    print_log("Start...")
    context.num = 8
    context.symbol = "AAA"
    # call PyCallGraph and Graphviz
    with PyCallGraph(output=GraphvizOutput()):
        context.model = test_model(context)

    schedule(schedule_func=algo, date_rule='1d', time_rule='09:31:00')


def test_model(context):
    model1 = GMModel()
    model1.add(AllSymbolSelector(list(index_list.keys())))
    model1.add(BlackFilter())
    # model1.add(WhiteFilter())
    # model1.add(TopNFilter(context.num))
    model1.add(GMOrder(context.num))

    model1.execute(context.now)
    return model1


def algo(context):
    print_log(context.now, " algo...")
    # last_day = get_previous_trading_date("SHSE", context.now)
    context.model.execute(context.now)


def on_backtest_finished(context, indicator):
    print_log(f"Done! From start, time elapsed: {time.time() - context.start_time} seconds")
    print_log(f"{context.symbol} backtest finished: ", indicator)


index_list = {
    # # SHSE
    # "SHSE.000001": "上证指数",
    # "SHSE.000002": "A股指数",
    # "SHSE.000004": "工业指数",
    # "SHSE.000005": "商业指数",
    # "SHSE.000006": "地产指数",
    # "SHSE.000007": "公用指数",
    # "SHSE.000008": "综合指数",
    # "SHSE.000009": "上证380",
    # "SHSE.000010": "上证180",
    # "SHSE.000015": "红利指数",
    "SHSE.000016": "上证50",
    # "SHSE.000017": "新综指",
    # "SHSE.000018": "180金融",
    # "SHSE.000300": "沪深300",
    # "SHSE 000903": "中证100",
    # "SHSE.000904": "中证200",
    # "SHSE.000905": "中证500",
    # "SHSE.000906": "中证800",
    # "SHSE.000907": "中证700",
    # "SHSE.000852": "中证1000",
    # # SZSE
    # "SZSE.399001": "深证成指",
    # "SZSE.399002": "深成指R",
    # "SZSE.399004": "深证100R",
    # "SZSE.399005": "中小板指",
    # "SZSE.399006": "中小板指",
    # "SZSE.399007": "深证300",
    # "SZSE.399008": "中小300",
    # "SZSE.399009": "深证200",
    # "SZSE.399010": "深证700",
    # "SZSE.399011": "深证1000",
    # "SZSE.399012": "创业300",
}

if __name__ == "__main__":
    run(
        strategy_id='9f53e15f-6870-11e8-801c-4cedfb681747',
        filename=(os.path.basename(__file__)),
        mode=MODE_BACKTEST,
        token='42c5e7778813e4a38aae2e65d70eb372ac8f2435',
        backtest_start_time="2014-08-01 09:30:00",
        backtest_end_time='2024-08-01 15:00:00',
        backtest_initial_cash=100000,
        backtest_adjust=ADJUST_PREV,
        backtest_slippage_ratio=0.01,
        backtest_commission_ratio=0.0005,
    )
