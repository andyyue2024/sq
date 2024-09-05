import numpy as np
import talib
from gm.api import *
from sq.utils import print_log
from sq.layers import *


class SingleFactor4Order(Order):
    """
    SingleFactor4Order order target.

    Main factors as follows:
    ----------------------
    - MACD close
    - buy when macd[-1] > 0 > macd[-2]
    - sell when macd[-1] < 0 < macd[-2]
    """

    def __init__(self, symbol = "SHSE.000300"):
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
                         end_time=last_day, fields="close", fill_missing="last", adjust=ADJUST_PREV, df=True)
        close = data["close"].values
        macdDIFF, macdDEA, macd = talib.MACD(close)

        if macd[-1] > 0 > macd[-2]:
            return OrderOp.BUY
        elif macd[-1] < 0 < macd[-2]:
            return OrderOp.SELL
        return super().get_order_op(target)

    def try_to_order(self, in_list: list) -> list:
        return super().try_to_order([self.symbol])



