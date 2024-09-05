from sq.gm.tools import *
from sq.layers import *


class SingleFactor5Order(Order):
    """
    SingleFactor5Order order target.

    Main factors as follows:
    ----------------------
    - rsrs_weight
    - buy when rsrs_weight > 0.7
    - sell when rsrs_weight < -0.7
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
        rsrs_weight = get_rsrs_weight(target, last_day)
        if rsrs_weight > 0.7:
            return OrderOp.BUY
        elif rsrs_weight < -0.7:
            return OrderOp.SELL
        return super().get_order_op(target)

    def try_to_order(self, in_list: list) -> list:
        return super().try_to_order([self.symbol])



