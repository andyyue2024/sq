from datetime import datetime, date
from sq import Model


class TuShareModel(Model):
    """
    TuShareModel
    """

    def __init__(self, *args):
        super().__init__(*args)

    def execute(self, now: str | datetime | date, **kwargs: object) -> object:
        return super().execute(now, **kwargs)
