from queue import Queue

import click
from book import Book
from consumer import Consumer
from producer import Producer


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option(
    "--file-path",
    required=True,
    type=str,
    help="File path to read from.",
)
@click.option(
    "--kafka-topic",
    required=True,
    type=str,
    help="Kafka topic to write into.",
)
def main(file_path: str, kafka_topic: str) -> None:
    buffer = Queue()
    book = Book()

    producer = Producer(file_path, buffer)
    consumer = Consumer(buffer, book)

    consumer.start()
    producer.start()

    producer.join()
    consumer.join()


if __name__ == "__main__":
    main()
