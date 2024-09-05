import time
from datetime import datetime, date

from sq.utils.log_util import print_log
from sq.models.core import BaseModel


class Model(BaseModel):
    """
    Model is a base class of group models.
    It is a group model or multi-models.

    Main Features
    -------------
    Here are just some features that Model can do well:
      - As a model, it can execute() and make layer to build().
      - As a group model, it can add more other models and make them to execute().
      - As a layer,it can build().
      - As a group layer, it can add more other layers and make them to build()
      - As a trainer,it can train() and predict().
      - As a group trainer, it can add more other trainers and make them to train() and predict()

    """

    def __init__(self, *args):
        super().__init__(*args)
        self._inner_models = []  # type: list[BaseModel]

    def execute(self, now: str | datetime | date, **kwargs) -> list:
        start_time = time.time()
        ret_list = []
        for model in self._inner_models:
            ret_list += model.execute(now, **kwargs)
        ret_list += super().execute(now, **kwargs)
        print_log(self.now, f" executing spend {time.time() - start_time} seconds")
        return ret_list

    def train(self, *args, **kwargs):
        for model in self._inner_models:
            model.train(*args, **kwargs)
        return super().train(*args, **kwargs)

    def predict(self, *args, **kwargs) -> list:
        ret_list = []
        for model in self._inner_models:
            ret_list += model.predict(*args, **kwargs)
        ret_list += super().predict(*args, **kwargs)
        return ret_list

    def add_model(self, model):
        # type: (Model) -> Model
        """
        add sub model to self.
        itself is a group model.
        :return:
        """
        if isinstance(model, BaseModel):
            self._inner_models.append(model)
        return self

    def clear_models(self):
        # type: () -> Model
        """
        clear models of itself.
        itself is a group model.
        :return:
        """
        self._inner_models.clear()
        return self






