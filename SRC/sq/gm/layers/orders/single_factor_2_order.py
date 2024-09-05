import numpy as np
import talib
from gm.api import *
from sq.utils import print_log
from sq.layers import *


class SingleFactor2Order(Order):
    """
    SingleFactor2Order order target.

    Main factors as follows:
    ----------------------
    - RSI close
    """

    def __init__(self, symbol = "SZSE.300296"):
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
        data = history_n(symbol=target, frequency="1d", count=35,
                         end_time=self.now, fields="open,high,low,close", fill_missing="last", adjust=ADJUST_PREV, df=True)
        # open = np.asarray((data["open"].values))
        # high = np.asarray((data["high"].values))
        # low = np.asarray((data["low"].values))
        close = np.asarray((data["close"].values))
        rsi = talib.RSI(close)
        rsi = rsi[-1]
        if rsi < 30:
            return OrderOp.BUY
        elif rsi > 70:
            return OrderOp.SELL
        return super().get_order_op(target)

    def try_to_order(self, in_list: list) -> list:
        return super().try_to_order([self.symbol])



