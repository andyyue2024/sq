from sq.gm.tools import *
from sq.layers import *


class SingleFactor6Order(Order):
    """
    SingleFactor6Order order target.

    Main factors as follows:
    ----------------------
    - pre_close of (close - open) OLS linear regression
    - buy when pre_close > data["open"].values
    - sell when others
    """

    def __init__(self, symbol = "SHSE.601318"):
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
        bias, weight = get_predict_close(target, self.now, count=7)
        data = history_n(target, frequency="1d", end_time=self.now, count=1, fields="open", df=True)
        pre_close = bias + weight * data["open"].values
        if pre_close > data["open"].values:
            return OrderOp.BUY
        else:
            return OrderOp.SELL
        # return super().get_order_op(target)

    def try_to_order(self, in_list: list) -> list:
        return super().try_to_order([self.symbol])



