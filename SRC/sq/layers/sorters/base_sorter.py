from abc import *

from sq.layers.layer import Layer


class Sorter(Layer):
    """
    Selector is a base class of sorters
    """
    def __init__(self, *args):
        super().__init__(*args)

    @abstractmethod
    def sort(self, in_list: list) -> list: ...
    """
    sort() is to sort target list from in_list by conditions
    """

    def build(self, in_list: list = None) -> list:
        sorted_list = self.sort(in_list)
        return super().build(sorted_list)
