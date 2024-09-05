import numpy as np
import talib
from gm.api import *
from sq.utils import print_log
from sq.layers import *


class SingleFactor3Order(Order):
    """
    SingleFactor3Order order target.

    Main factors as follows:
    ----------------------
    - Dual Thrust 轨道突破策略
    """
    count = 25
    k1 = 0.7
    flag = 100
    flag_check = 2

    def __init__(self, symbol = "SHSE.600000"):
        super().__init__()
        self.symbol = symbol

    def sell_target(self, target: str):
        super().sell_target(target)
        order_target_percent(symbol=target, percent=0, order_type=OrderType_Market,
                             position_side=PositionSide_Long)

    def buy_target(self, target: str):
        super().buy_target(target)
        order_target_percent(symbol=target, percent=1., order_type=OrderType_Market,
                             position_side=PositionSide_Long)

    def get_order_op(self, target: str) -> OrderOp:
        last_day = get_previous_trading_date("SHSE", self.now)
        data = history_n(symbol=target, frequency="1d", count=35,
                         end_time=last_day, fields="open,high,low,close", fill_missing="last", adjust=ADJUST_PREV, df=True)
        high = np.asarray((data["high"].values))
        low = np.asarray((data["low"].values))
        close = np.asarray((data["close"].values))

        hh = np.max(high)
        hc = np.max(close)
        lc = np.min(close)
        ll = np.min(low)

        max_range = np.max([hh - hc, lc - ll])
        data_now = current(symbols=target)[0]
        data_now_open = data_now["open"]
        data_now_price = data_now["price"]
        range_up_price = data_now_open + SingleFactor3Order.k1 * max_range
        if data_now_price > range_up_price:
            return OrderOp.BUY
        elif data_now_price < range_up_price:
            return OrderOp.SELL
        return super().get_order_op(target)

    def try_to_order(self, in_list: list) -> list:
        return super().try_to_order([self.symbol])



