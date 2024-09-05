from sq.gm.tools import *
from sq.layers import Filter


class BlackFilter(Filter):
    """
    BlackFilter remove items in black list from original targets
    """

    def __init__(self, black_list: list = None, black_index_list: list = None):
        super().__init__()
        self._black_list = []
        self._black_index_list = []

        if black_list is not None:
            self._black_list.extend(black_list)
        if black_index_list is None:
            black_index_list = ["SHSE.000947", "SZSE.399975", "SHSE.000948"]  # default add 3 black index.
        self._black_index_list.extend(black_index_list)

    def filter(self, in_list: list):
        symbol_list = filter_black_list(in_list, self.now, self._black_index_list)
        symbol_list = [item for item in symbol_list if item not in self._black_list]
        return symbol_list
