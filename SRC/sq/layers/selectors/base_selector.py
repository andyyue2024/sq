from abc import *

from sq.layers.layer import Layer


class Selector(Layer):
    """
    Selector is a base class of selectors
    """
    def __init__(self, *args):
        super().__init__(*args)

    @abstractmethod
    def select(self, in_list: list) -> list: ...
    """
    select() is to select target list from in_list by conditions
    """

    def build(self, in_list: list = None) -> list:
        selected_list = self.select(in_list)
        return super().build(selected_list)
