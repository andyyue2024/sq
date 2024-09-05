from gm.api import *

from sq.layers import *


class GMOrder(Order):
    """
    GMOrder order targets by percent(=1. / max_count)
    """

    def __init__(self, max_count: int = 10, *args):
        super().__init__(*args)
        self._max_count = max_count

    @property
    def max_count(self):
        return self._max_count

    def sell_target(self, target: str):
        super().sell_target(target)
        order_target_percent(symbol=target, percent=0, order_type=OrderType_Market,
                             position_side=PositionSide_Long)

    def buy_target(self, target: str):
        super().buy_target(target)
        order_target_percent(symbol=target, percent=1. / self.max_count, order_type=OrderType_Market,
                             position_side=PositionSide_Long)

    def get_order_op(self, target: str) -> OrderOp:
        # return super().get_order_op(target)
        return OrderOp.BUY

    def try_to_order(self, in_list: list) -> list:
        order_close_all()
        return super().try_to_order(in_list)
