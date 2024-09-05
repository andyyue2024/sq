from gm.api import *

from sq.utils import print_log
from sq.layers import *


class AverageOrder(Order):
    """
    AverageOrder order targets by percent(=1. / max_count)
    """

    def __init__(self, *args):
        super().__init__(*args)
        self._max_count = 1

    @property
    def max_count(self):
        return self._max_count

    def sell_target(self, target: str):
        super().sell_target(target)

    def buy_target(self, target: str):
        super().buy_target(target)
        order_target_percent(symbol=target, percent=1. / self.max_count, order_type=OrderType_Market,
                             position_side=PositionSide_Long)

    def get_order_op(self, target: str) -> OrderOp:
        return OrderOp.BUY

    def try_to_order(self, in_list: list) -> list:
        order_close_all()
        self._max_count = len(in_list)
        print_log("max_count: ", self.max_count)
        return super().try_to_order(in_list)
