from sq.layers.layer import Layer
from sq.layers.orders.abstract_order import AbstractOrder
from sq.layers.orders.order_op import OrderOp
from sq.utils import print_log


class Order(Layer, AbstractOrder):
    """
    Order is a base class of orders
    """
    def __init__(self, *args):
        super().__init__(*args)

    def try_to_order(self, in_list: list) -> list:
        hold_target_list = []
        for target in in_list:
            oo = self.get_order_op(target)
            if OrderOp.BUY == oo:
                self.buy_target(target)
                hold_target_list.append(target)
            elif OrderOp.SELL == oo:
                self.sell_target(target)
                if target in hold_target_list:
                    hold_target_list.remove(target)
            elif OrderOp.NOTHING == oo:
                pass
        return hold_target_list

    def get_order_op(self, target: str) -> OrderOp:
        return OrderOp.NOTHING

    def buy_target(self, target: str):
        print_log("buy_target: ", target)

    def sell_target(self, target: str):
        print_log("sell_target: ", target)

    def build(self, in_list: list = None) -> list:
        hold_target_list = self.try_to_order(in_list)
        return super().build(hold_target_list)
