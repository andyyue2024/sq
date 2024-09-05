from datetime import datetime, date

from sq.layers import Layer
from sq.models.core.abstract_model import AbstractModel
from sq.trainers import Trainer


class BaseModel(AbstractModel, Layer, Trainer):
    """
    BaseModel is a base class of model classes
    It is a single model.
    """

    def __init__(self, *args):
        Layer.__init__(self, *args)
        Trainer.__init__(self)

    def execute(self, now: str | datetime | date, **kwargs) -> list:
        """
        execute model
        :param now: current date of time tick when schedule()
        :param kwargs:
        :return: result list
        """
        # super().execute(now, **kwargs)
        self.setTimeTick(now)
        ret_list = super().build()
        return ret_list

    # def train(self, *args, **kwargs):
    #     return super().train(*args, **kwargs)
    #
    # def predict(self, *args, **kwargs) -> list:
    #     return super().predict(*args, **kwargs)

    def do_predicting(self, *args, **kwargs):
        pass

    def do_training(self, *args, **kwargs):
        pass

