from abc import *
from datetime import datetime, date


class AbstractModel(ABC):
    """
    AbstractModel is abstract class of model classes
    """
    @abstractmethod
    def execute(self, now: str | datetime | date, **kwargs) -> list:
        """
        execute model
        :param now: current date of time tick when schedule()
        :param kwargs:
        :return: result list
        """