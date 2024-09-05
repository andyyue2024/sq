import numpy as np
from gm.api import *

from sq.utils import print_log
from sq.layers import *


class SVMOrder(Order):
    """
    SVMOrder order targets by prediction of SVM
    """

    def __init__(self, context, model, *args):
        super().__init__(*args)
        self.context = context
        self.model = model

    def sell_target(self, target: str):
        super().sell_target(target)
        order_close_all()
        # order_target_percent(symbol=target, percent=0, order_type=OrderType_Market, position_side=PositionSide_Long)

    def buy_target(self, target: str):
        super().buy_target(target)
        order_target_percent(symbol=target, percent=0.95, order_type=OrderType_Market, position_side=PositionSide_Long)

    def get_order_op(self, target: str) -> OrderOp:
        recent_data = history_n(target, frequency='1d', end_time=self.now, count=2,
                                fields="open,close,high,low,volume", fill_missing='last', df=True)
        bar_close = recent_data['close'].values
        # 获取数据并计算相应的因子
        # 于星期一的09:31:00进行操作
        # 当前bar的工作日
        weekday = self.now.isoweekday()
        # 获取模型相关的数据
        # 获取持仓
        # 如果日期是新的星期一且没有仓位则开始预测
        position = self.context.account().position(symbol=target, side=PositionSide_Long)
        if not position and self.model and weekday == 1:
            predictions = self.model.predict()
            prediction = sum(predictions) / len(predictions)
            # 若预测值为上涨则开仓
            if prediction == 1:
                return OrderOp.BUY

        # 当涨幅大于10%,平掉所有仓位止盈
        elif position and bar_close[-1] / bar_close[0] >= 1.10:
            # print_log(f'      {target}以市价单全平多仓止盈')
            return OrderOp.SELL

        # 当时间为周五并且跌幅大于2%时,平掉所有仓位止损
        elif position and bar_close[-1] / bar_close[0] < 1.02 and weekday == 5:
            # print_log(f'      {target}以市价单全平多仓止损')
            return OrderOp.SELL
        return super().get_order_op(target)
