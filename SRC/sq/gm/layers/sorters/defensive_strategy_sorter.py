from sq.gm.tools import *
from sq.layers import Sorter


class DefensiveStrategySorter(Sorter):
    """
    DefensiveStrategySorter filter and sort original targets.

    Main factors as follows:
    ----------------------
    - 排名条件设市盈率从小到大，权重2；  PETTM
    - 股息率从大到小，权重1； DY
    - 市净率从小到大，权重3； PB
    - 历史贝塔从小到大，权重2；
    - 自定义波动率指标从小到大权重10，
    Sort by:
    ----------------------
    - weight score of all factors

    """

    def __init__(self):
        super().__init__()

    def sort(self, in_list: list) -> list:
        return defensive_strategy2(list(in_list), self.now)


