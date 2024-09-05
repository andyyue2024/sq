import numpy as np
import pandas as pd
from gm.api import *

from sq.utils import print_log
from sq.gm.tools import get_time_Ymd
from sq.layers import *


class ManualOrder(Order):
    """
    SVMOrder order targets by prediction of SVM
    """
    FILE_PATH_FLAG_SH = "./data/flag_sh.xlsx"

    def __init__(self, context, model=None, *args):
        super().__init__(*args)
        self.context = context
        self.model = model
        if model is None:
            df = pd.read_excel(ManualOrder.FILE_PATH_FLAG_SH)
            column1 = df['eob']
            column2 = df['hold']
            # using zip() to make key-value，and than transfer to dict
            self.flag_dict = dict(zip(column1, column2))

    def sell_target(self, target: str):
        super().sell_target(target)
        order_close_all()
        # order_target_percent(symbol=target, percent=0, order_type=OrderType_Market, position_side=PositionSide_Long)

    def buy_target(self, target: str):
        super().buy_target(target)
        order_target_percent(symbol=target, percent=1.0, order_type=OrderType_Market, position_side=PositionSide_Long)

    def get_order_op_by_origin_flag_data(self, target: str) -> OrderOp:
        flag = self.flag_dict.get(get_time_Ymd(self.now))
        if 1 == flag:
            return OrderOp.BUY
        elif 0 == flag:
            return OrderOp.SELL
        return super().get_order_op(target)

    def get_order_op(self, target: str) -> OrderOp:
        if self.model is None:  # check flag in flag_dict as default
            return self.get_order_op_by_origin_flag_data(target)
        position = self.context.account().position(symbol=target, side=PositionSide_Long)
        predictions = self.model.predict(now=self.now)
        print_log("predictions: ", predictions)
        if len(predictions) == 0:
            return super().get_order_op(target)
        prediction = np.asarray(predictions).mean()
        if not position and prediction == 1:
            return OrderOp.BUY
        elif position and prediction == 0:
            return OrderOp.SELL
        # print_log("position: ", position)
        return super().get_order_op(target)
