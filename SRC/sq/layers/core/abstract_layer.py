from abc import *


class AbstractLayer[T](ABC):
    """
    AbstractLayer is abstract class for layer classes
    It defines core method build(), which implement logic function.
    """

    @abstractmethod
    def build(self, in_list: list[T] = None) -> list[T]: ...
    """
    core method
    """

