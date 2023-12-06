import os

import pika

QUEUE_TTL = 15 * 60 * 1000


class RabbitmqConsumer:
    def __init__(self, queue, callback) -> None:
        self.__host = os.environ.get('RABBITMQ_HOST', 'localhost')
        self.__port = os.environ.get('RABBITMQ_PORT', 5672)
        self.__usernamer = os.environ.get('RABBITMQ_USERNAME', 'bugs')
        self.__password = os.environ.get('RABBITMQ_PASSWORD', 'bunny')
        self.__queue = queue
        self.__callback = callback
        self.channel = self.__create_channel()

    def __create_channel(self):
        connection_parameters = pika.ConnectionParameters(
            host=self.__host,
            port=self.__port,
            credentials=pika.PlainCredentials(
                username=self.__usernamer, password=self.__password
            ),
        )
        channel = pika.BlockingConnection(connection_parameters).channel()
        channel.queue_declare(
            queue=self.__queue,
            durable=False,
            arguments={'x-expires': QUEUE_TTL},
        )
        channel.stop_consuming()
        channel.basic_consume(
            queue=self.__queue,
            auto_ack=True,
            on_message_callback=self.__callback,
        )
        return channel

    def start(self):
        self.channel.start_consuming()
