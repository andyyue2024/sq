from abc import *

from sq.layers.layer import Layer


class Merge(Layer):
    """
    Merge is a base class of merging
    """
    def __init__(self, *args):
        super().__init__(*args)

    @abstractmethod
    def merge(self, in_list: list) -> list: ...
    """
    merge() is to merge target list with in_list by conditions
    """

    def build(self, in_list: list = None) -> list:
        merged_list = self.merge(in_list)
        return super().build(merged_list)
