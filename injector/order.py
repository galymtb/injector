from side import Side
from type import Type


class Order:
    def __init__(
        self,
        timestamp: str,
        id: str,
        symbol: str,
        side: str,
        type: str,
        price: str,
        quantity: str,
    ) -> None:
        self._timestamp: str = timestamp
        self._id: str = id
        self._symbol: str = symbol

        try:
            self._side: Side = Side(side)
            self._type: Type = Type(type)
        except Exception:
            pass

        self._price: float = float(price)
        self._quantity: int = int(quantity)

    def __repr__(self) -> str:
        return (
            f"Order(id={self._id}, symbol={self._symbol}, side={self._side}, "
            f"type={self._type}, price={self._price}, quantity={self._quantity}, "
            f"ts={self._timestamp})"
        )
