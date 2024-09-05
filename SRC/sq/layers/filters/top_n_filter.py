from sq.layers.filters import Filter


class TopNFilter(Filter):
    """
    TopNFilter filter the top n targets
    """

    def __init__(self, top_count: int, *args):
        super().__init__(*args)
        self._top_count = top_count

    def filter(self, in_list: list):
        if not in_list:
            return []
        return in_list[0:self._top_count]




