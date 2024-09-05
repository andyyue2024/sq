from sq.gm.tools import *
from sq.layers import Selector


class AllSymbolSelector(Selector):
    """
    AllSymbolSelector remove items in black list from original targets
    """

    def __init__(self, index_list: list):
        super().__init__()
        self._index_list = []
        if index_list is not None:
            self._index_list.extend(index_list)

    @property
    def index_list(self):
        return self._index_list

    def select(self, in_list: list):
        symbol_list = get_symbol_list_from_indexes(self.index_list, self.now)
        return symbol_list
