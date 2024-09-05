from sq.gm.tools import *
from sq.layers import Filter


class PermanentBlackFilter(Filter):
    """
    PermanentBlackFilter remove items in black list from original targets
    black list will increase only.
    """

    def __init__(self, black_list: list = None):
        super().__init__()
        self._black_list = []
        if black_list is not None:
            self._black_list.extend(black_list)

    def filter(self, in_list: list):
        symbol_list = [item for item in in_list if item not in self._black_list]
        return symbol_list
