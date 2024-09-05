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
    context.symbol = "test_model_6_2"
    context.model = test_model_6_2(context)

    schedule(schedule_func=algo, date_rule='1m', time_rule='09:31:00')


def test_model_6_2(context):
    model1 = GMModel()
    model1.add(AllSymbolSelector(list(index_list.keys())))
    model1.add(SingleFactor1Sorter("NPGRT", False))  # 因子 归属母公司净利润增长率NPGRT
    model1.add(TopNFilter(context.num))
    model1.add(GMOrder(context.num))
    model1.execute(context.now)
    # 1.For SHSE.000016
    # every executing spend about 1 seconds. And from 2014-08-01 to 2016-08-01, it spends about 24 seconds.
    # test_model_6_2 backtest finished:
    #           {'account_id': '9f53e15f-6870-11e8-801c-4cedfb681747', 'pnl_ratio': -0.11928160445503701,
    #            'pnl_ratio_annual': -0.05947784921596791, 'sharp_ratio': -0.10341200074895916,
    #            'max_drawdown': 0.6351411087007472, 'risk_ratio': 0.8600677426966857, 'open_count': 204,
    #            'close_count': 197, 'win_count': 88, 'lose_count': 109, 'win_ratio': 0.4467005076142132,
    #            'calmar_ratio': -0.09364509461155263, 'created_at': None, 'updated_at': None}
    # every executing spend about 1 seconds. And from 2014-08-01 to 2024-08-01, it spends about 135 seconds.
    # test_model_6_2 backtest finished:
    #           {'account_id': '9f53e15f-6870-11e8-801c-4cedfb681747', 'pnl_ratio': -0.6680646424504169,
    #            'pnl_ratio_annual': -0.06673333182660157, 'sharp_ratio': -0.23915632332097173,
    #            'max_drawdown': 0.8507123962204256, 'risk_ratio': 0.27120129599007015, 'open_count': 817,
    #            'close_count': 814, 'win_count': 331, 'lose_count': 483, 'win_ratio': 0.40663390663390664,
    #            'calmar_ratio': -0.0784440571491455, 'created_at': None, 'updated_at': None}
    # 2.For index_list
    # every executing spend about 57 seconds. And from 2014-08-01 to 2016-08-01, it spends about 1380 seconds.
    # test_model_6_2 backtest finished:
    #           {'account_id': '9f53e15f-6870-11e8-801c-4cedfb681747', 'pnl_ratio': 1.0257895138919877,
    #            'pnl_ratio_annual': 0.5114934051510595, 'sharp_ratio': 0.5067588727594312,
    #            'max_drawdown': 0.5790127998741605, 'risk_ratio': 0.9821829021880045, 'open_count': 207,
    #            'close_count': 199, 'win_count': 116, 'lose_count': 83, 'win_ratio': 0.5829145728643216,
    #            'calmar_ratio': 0.8833887700966622, 'created_at': None, 'updated_at': None}
    # every executing spend about 47 seconds. And from 2014-08-01 to 2024-08-01, it spends about 5941 seconds.
    # test_model_6_2 backtest finished:
    #           {'account_id': '9f53e15f-6870-11e8-801c-4cedfb681747', 'pnl_ratio': -0.1771726584763809,
    #            'pnl_ratio_annual': -0.01769787092060181, 'sharp_ratio': -0.03174158637486728,
    #            'max_drawdown': 0.8181090009210107, 'risk_ratio': 0.8276618611381636, 'open_count': 961,
    #            'close_count': 954, 'win_count': 426, 'lose_count': 528, 'win_ratio': 0.44654088050314467,
    #            'calmar_ratio': -0.021632656407248794, 'created_at': None, 'updated_at': None}

    return model1



def algo(context):
    print_log(context.now, " algo...")
    # last_day = get_previous_trading_date("SHSE", context.now)
    context.model.execute(context.now)


def on_backtest_finished(context, indicator):
    print_log(f"Done! From start, time elapsed: {time.time() - context.start_time} seconds")
    print_log(f"{context.symbol} backtest finished: ", indicator)


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
        backtest_end_time='2024-08-01 15:00:00',
        backtest_initial_cash=100000,
        backtest_adjust=ADJUST_PREV,
        backtest_slippage_ratio=0.01,
        backtest_commission_ratio=0.0005,
    )
