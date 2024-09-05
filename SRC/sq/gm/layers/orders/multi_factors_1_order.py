from sq.gm.tools import *
from sq.layers import *


class MultiFactors1Order(Order):
    """
    MultiFactors1Order order target.

    Main factors as follows:
    ----------------------
    - pre_close of (close - open) OLS linear regression
    - buy when (close[-1] > upBand) and (current_price > buyPoint)
    - sell when (close[-1] < lowBand) and (current_price < sellPoint)
    """
    ceilingAmt = 60
    floorAmt = 20
    bolBandTrig = 1
    lookBackDays = 30
    
    
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
        data = history_n(symbol=target, frequency="1d", count=int(MultiFactors1Order.lookBackDays),
                         end_time=last_day, fields="open,high,low,close,volume",
                         fill_missing="last", adjust=ADJUST_PREV, df=True)
        close = np.asarray((data["close"].values))
        high = np.asarray((data["high"].values))
        low = np.asarray((data["low"].values))
        # todayVolatility = np.std(close)
        # yesterDayVolatility = np.std(close[:-1])
        # deltaVolatility = (todayVolatility - yesterDayVolatility) / todayVolatility
        # lookBackDays = np.round(MultiFactors1Order.lookBackDays * (1 + deltaVolatility))
        # lookBackDays = np.min([lookBackDays, MultiFactors1Order.ceilingAmt])
        # lookBackDays = np.max([lookBackDays, MultiFactors1Order.floorAmt])

        MidLine = np.average(close)
        Band = np.std(close)
        upBand = MidLine + MultiFactors1Order.bolBandTrig * Band
        lowBand = MidLine - MultiFactors1Order.bolBandTrig * Band

        buyPoint = np.max(high)
        sellPoint = np.min(low)
        current_data = current(symbols=target)
        current_price = current_data[0]["price"]
        
        if (close[-1] > upBand) and (current_price > buyPoint):
            return OrderOp.BUY
        if (close[-1] < lowBand) and (current_price < sellPoint):
            return OrderOp.SELL
        # return super().get_order_op(target)

    def try_to_order(self, in_list: list) -> list:
        return super().try_to_order([self.symbol])



