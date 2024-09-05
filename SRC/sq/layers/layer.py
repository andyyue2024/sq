from sq.layers.core import BaseLayer


class Layer(BaseLayer[str]):
    """
    Layer is base class of group layers
    It is a group layer or multilayer
    """

    def __init__(self, *args):
        super().__init__()
        self._inner_layers = []  # type: list[BaseLayer]
        for arg in args:
            if isinstance(arg, BaseLayer):
                self.add(arg)

    def setTimeTick(self, value):
        super().setTimeTick(value)
        for layer in self._inner_layers:
            layer.setTimeTick(value)

    def build(self, in_list: list = None) -> list:
        """
        Core method.
        For group layers, first call build() of inner layers;
        and then call itself build() to store.
        :param in_list:
        :return:
        """
        ret_list = in_list
        for layer in self._inner_layers:
            ret_list = layer.build(ret_list)
        return super().build(ret_list)

    def add(self, layer):
        # type: (Layer) -> Layer
        """
        add layer to self.
        itself is a group layer.
        :return:
        """
        if isinstance(layer, BaseLayer):
            self._inner_layers.append(layer)
        return self

    def clear(self):
        # type: () -> Layer
        """
        clear layers of itself.
        itself is a group layer.
        :return:
        """
        self._inner_layers.clear()
        return self
