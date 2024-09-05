from datetime import datetime, date
from typing import Any
from sq.utils import print_log
from sq.trainers.core import AbstractTrainer


class BaseTrainer[T](AbstractTrainer):
    """
    BaseTrainer ia a base class of trainer classes
    It is a single trainer
    """

    def __init__(self, target: str = None, start_date: str | datetime | date = None,
                 end_date: str | datetime | date = None, now: str | datetime | date = None):
        super().__init__()
        #  current date of time tick when schedule()
        self._target = target
        self._start_date = start_date
        self._end_date = end_date
        self._now = now
        self._clf = None
        # prediction of trainer when time tick(now).
        self._prediction: Any = None

    @property
    def target(self):
        return self._target

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @property
    def now(self):
        return self._now

    @property
    def clf(self):
        return self._clf

    @clf.setter
    def clf(self, value):
        self._clf = value
        print_log(self.__class__.__name__, ", _clf: ", self._clf, level='DEBUG')

    @property
    def prediction(self):
        return self._prediction

    @prediction.setter
    def prediction(self, value):
        self._prediction = value
        print_log(self.__class__.__name__, ", prediction: ", self._prediction, level='DEBUG')

    def train(self, *args, **kwargs):
        # type: (list,  dict) -> BaseTrainer
        """
        train models according input data
        :return:
        """
        return self

    def predict(self, *args, **kwargs) -> list:
        """
        predict result.
        add self.prediction to a list and return the list
        :param args:
        :param kwargs:
        :return:
        """
        if self.prediction is None:
            return []
        return [self.prediction]
