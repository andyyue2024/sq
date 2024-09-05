from abc import *
from typing import Any


class AbstractTrainer(ABC):
    """
    AbstractTrainer is abstract class of trainer classes
    It defines core method train(), which implement logic function.
    """

    @abstractmethod
    def train(self, *args, **kwargs) -> Any: ...
    """
    train models according input data
    :return:
    """

    @abstractmethod
    def predict(self, *args, **kwargs) -> list: ...
    """
    predict result.
    :param args:
    :param kwargs:
    :return:
    """




