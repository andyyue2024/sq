from sq.layers.core.abstract_layer import AbstractLayer
from sq.utils import print_log


class BaseLayer[T](AbstractLayer):
    """
    BaseLayer is a base class for layer classes.
    It is a single layer
    """

    def __init__(self):
        super().__init__()
        # store the result of current layer after build()
        self._target_list = [T]
        #  current date of time tick when schedule()
        self._now = 0

    @property
    def now(self):
        return self._now

    @now.setter
    def now(self, value):
        self._now = value
        print_log(self.__class__.__name__, ", time tick: ", self._now, level='DEBUG')

    def setTimeTick(self, value):
        self.now = value

    def build(self, in_list: list[T] = None) -> list[T]:
        """
        Core method.
        For single layer, just add all items of in_list to self.target_list
        :param in_list:
        :return:
        """
        self._target_list.clear()
        if in_list:
            self._target_list.extend(in_list)
        print_log(self.__class__.__name__, ", target list len: ", len(self._target_list), level='DEBUG')
        return list(self._target_list)
