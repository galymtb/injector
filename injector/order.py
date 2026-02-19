from side import Side
from type import Type


class Order:
    _timestamp: str
    _id: str
    _symbol: str
    _side: Side
    _type: Type
    _price: float
    _quantity: int

    def __init__(
        self,
        timestamp: str,
        order_id: str,
        order_symbol: str,
        order_side: str,
        order_type: str,
        order_price: str,
        order_quantity: str,
    ):
        self._timestamp = timestamp
        self._id = order_id
        self._symbol = order_symbol

        try:
            self._side = Side(order_side)
            self._type = Type(order_type)
        except Exception:
            pass

        self._price = float(order_price)
        self._quantity = int(order_quantity)

    def __repr__(self) -> str:
        return (
            f"Order(id={self._id}, symbol={self._symbol}, side={self._side}, "
            f"type={self._type}, price={self._price}, quantity={self._quantity}, "
            f"ts={self._timestamp})"
        )
