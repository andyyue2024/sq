from abc import *
from sq.layers.layer import Layer


class Filter(Layer):
    """
    Filter is a base class of filters
    """
    def __init__(self, *args):
        super().__init__(*args)

    @abstractmethod
    def filter(self, in_list: list) -> list: ...
    """
    filter() is to filter in_list by conditions
    """

    def build(self, in_list: list = None) -> list:
        filtered_list = self.filter(in_list)
        return super().build(filtered_list)




