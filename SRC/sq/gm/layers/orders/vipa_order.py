from sq.gm.tools import *
from sq.layers import *


class VIPAOrder(Order):
    """
    VIPAOrder order targets by percent(=1. / max_count)
    """

    def __init__(self, context, max_count: int = 10, *args):
        super().__init__(*args)
        self._max_count = max_count
        self.context = context
        self.black_target_list = []

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
        if sell_check(self.now, target):
            self.black_target_list.append(target)
            return OrderOp.SELL
        if (target not in self.black_target_list) and (buy_check(self.now, target)):
            return OrderOp.BUY
        return super().get_order_op(target)

    def try_to_order_for_holdings(self) :
        positions = self.context.account().positions()
        hold_target_list = get_data_value(positions, "symbol")
        for target in hold_target_list:
            if sell_check(self.now, target):
                self.black_target_list.append(target)
                self.sell_target(target)

    def try_to_order(self, in_list: list) -> list:
        self.try_to_order_for_holdings()

        hold_target_list = []
        for target in in_list:
            if (target not in self.black_target_list) and (buy_check(self.now, target)):
                self.buy_target(target)
                hold_target_list.append(target)
        return hold_target_list



