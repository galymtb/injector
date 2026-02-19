from queue import Queue
from threading import Thread

POISON_PILL = "END"


class Producer(Thread):
    _file_path: str
    _buffer: Queue

    def __init__(self, file_path: str, buffer: Queue):
        super().__init__(daemon=True)
        self._file_path = file_path
        self._buffer = buffer

    def run(self):
        try:
            for row in self._read_file(self._file_path):
                self._buffer.put(row)
        finally:
            self._buffer.put(POISON_PILL)

    def _read_file(self, file_path: str):
        with open(file_path, newline="", encoding="utf-8") as file:
            for row in file:
                row = row.strip()
                row = row.split()
                yield row
