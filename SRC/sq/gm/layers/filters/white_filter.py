from sq.layers import Filter


class WhiteFilter(Filter):
    """
    WhiteFilter add items of white list to original targets
    """

    def __init__(self, white_list: list = None):
        super().__init__()
        self._white_list = list(white_list)

    def filter(self, in_list: list):
        if in_list is None:
            in_list = []
        return in_list + [item for item in self._white_list if item not in in_list]

