from datetime import datetime, date

from sq.trainers.core import BaseTrainer


class Trainer(BaseTrainer):
    """
    Trainer is base class of group trainers
    It is a group trainer or multi-trainers
    """

    def __init__(self, target: str = None, start_date: str | datetime | date = None,
                 end_date: str | datetime | date = None, now: str | datetime | date = None):
        super().__init__(target, start_date, end_date, now)
        self._inner_trainers = []  # type: list[BaseTrainer]

    def train(self, *args, **kwargs):
        self.do_training(*args, **kwargs)
        for trainer in self._inner_trainers:
            trainer.train(*args, **kwargs)
        super().train(*args, **kwargs)
        return self

    def do_training(self, *args, **kwargs):
        """
        do training
        :param args:
        :param kwargs:
        example:
        # for arg in args:
        #     print(arg)
        # for key, value in kwargs.items():
        #     print(f"{key} = {value}")
        if kwargs:
            self._now = kwargs.get("now")
            self._target = kwargs.get("target")
            self._start_date = kwargs.get("start_date")
            self._end_date = kwargs.get("end_date")
        self.clf = 0
        self._clf = ...
        """
        raise NotImplementedError(
            f"Model {self.__class__.__name__} does not have a `do_training()` "
            "method implemented."
        )

    def predict(self, *args, **kwargs) -> list:
        self.do_predicting(*args, **kwargs)
        ret_list = []
        for trainer in self._inner_trainers:
            ret_list += trainer.predict(*args, **kwargs)
        ret_list += super().predict(*args, **kwargs)
        return ret_list

    def do_predicting(self, *args, **kwargs):
        """
        to do predicting.
        :param args:
        :param kwargs:
        example:
        features = [close_mean, volume_mean, max_mean, min_mean, vol, return_now, std]
        self.prediction = self._clf.predict(features)[0]
        self.prediction = ...
        """
        raise NotImplementedError(
            f"Model {self.__class__.__name__} does not have a `do_predicting()` "
            "method implemented."
        )

    def add_trainer(self, trainer):
        # type: (Trainer) -> Trainer
        """
        add sub trainer to self.
        itself is a group trainer.
        :return:
        """
        if isinstance(trainer, BaseTrainer):
            self._inner_trainers.append(trainer)
        return self

    def clear_trainers(self):
        # type: () -> Trainer
        """
        clear trainers of itself.
        itself is a group trainer.
        :return:
        """
        self._inner_trainers.clear()
        return self
