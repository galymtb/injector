from queue import Queue
from threading import Thread

POISON_PILL = "END"


class Producer(Thread):
    def __init__(self, file_path: str, buffer: Queue) -> None:
        super().__init__(daemon=True)
        self._file_path: str = file_path
        self._buffer: Queue = buffer

    def _read(self, file_path: str):
        with open(file_path, newline="", encoding="utf-8") as file:
            for row in file:
                row = row.strip()
                row = row.split()
                yield row

    def run(self):
        try:
            for row in self._read(self._file_path):
                self._buffer.put(row)
        finally:
            self._buffer.put(POISON_PILL)
