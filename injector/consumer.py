from queue import Queue
from threading import Thread

from book import Book
from order import Order

POISON_PILL = "END"


class Consumer(Thread):
    def __init__(self, buffer: Queue, book: Book):
        super().__init__(daemon=True)
        self._buffer: Queue = buffer
        self._book: Book = book

    def _process(self, order: Order) -> None:
        match order._type:
            case "NEW":
                self._book.on_new(order)
            case "CANCEL":
                self._book.on_cancel(order)
            case "TRADE":
                self._book.on_trade(order)
            case _:
                return
        print(self._book)

    def run(self):
        while True:
            item = self._buffer.get()
            if item is POISON_PILL:
                break
            order = Order(*item)
            if order._id != "0":
                self._process(order)
