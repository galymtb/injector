from collections import OrderedDict
from decimal import Decimal
from typing import Dict

from order import Order
from side import Side


class Book:
    def __init__(self):
        self._bids: Dict[Decimal, OrderedDict[str, Order]] = {}
        self._asks: Dict[Decimal, OrderedDict[str, Order]] = {}

    def _get_book_side(self, side: Side) -> Dict[Decimal, OrderedDict[str, Order]]:
        return self._bids if side == Side.BUY else self._asks

    def _exists(self, price: Decimal, order_id: int, side: str) -> bool:
        book = self._get_book_side(side)
        return price in book and order_id in book[price]

    def _decrease_quantity(
        self, price: Decimal, order_id: int, qty: int, side: str
    ) -> None:
        book = self._get_book_side(side)
        if price not in book:
            return

        orders_at_price = book[price]
        if order_id not in orders_at_price:
            return

        order_in_book = orders_at_price[order_id]

        if qty >= order_in_book._quantity:
            del orders_at_price[order_id]
        else:
            order_in_book._quantity -= qty

        if not orders_at_price:
            del book[price]

    def on_new(self, order: Order) -> None:
        book = self._get_book_side(order._side)
        if order._price not in book:
            book[order._price] = {}
        book[order._price][order._id] = order

    def on_cancel(self, order: Order) -> None:
        self._decrease_quantity(order._price, order._id, order._quantity, order._side)

    def on_trade(self, order: Order) -> None:
        self._decrease_quantity(order._price, order._id, order._quantity, order._side)

    def get_best_bid(self):
        if not self._bids:
            return None
        best_price = max(self._bids.keys())
        orders_at_price = self._bids[best_price]
        total_qty = 0
        for order in orders_at_price.values():
            total_qty += order._quantity
        return best_price, total_qty

    def get_best_ask(self):
        if not self._asks:
            return None
        best_price = min(self._asks.keys())
        orders_at_price = self._asks[best_price]
        total_qty = 0
        for order in orders_at_price.values():
            total_qty += order._quantity
        return best_price, total_qty

    def __str__(self):
        return f"Best bid: {self.get_best_bid()} | Best offer: {self.get_best_ask()}"
