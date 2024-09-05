from abc import *
from sq.layers.orders.order_op import OrderOp


class AbstractOrder(ABC):
    """
    Abstract is abstract class of order classes
    """

    @abstractmethod
    def try_to_order(self, target_list: list) -> list:
        """
        try to order
        :param target_list:
        :return: increased hold target
        """
        pass

    @abstractmethod
    def get_order_op(self, target: str) -> OrderOp:
        """
        get direction of order operation
        :param target:
        """
        pass

    @abstractmethod
    def buy_target(self, target: str):
        """
        buy target
        :param target:
        """
        pass

    @abstractmethod
    def sell_target(self, target: str):
        """
        sell target
        :param target:
        """
        pass
