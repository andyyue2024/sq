from datetime import datetime, date

from sq.models import Model


class GMModel(Model):
    """
    GMModel
    """

    def __init__(self, *args):
        super().__init__(*args)

    def execute(self, now: str | datetime | date, **kwargs: object) -> object:
        return super().execute(now, **kwargs)
