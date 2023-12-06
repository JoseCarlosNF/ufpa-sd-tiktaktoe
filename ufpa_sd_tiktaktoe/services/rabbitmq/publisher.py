import json
import os

import pika

QUEUE_TTL = 15 * 60 * 1000


class RabbitmqPublisher:
    def __init__(self, routing_key: str) -> None:
        self.__host = os.environ.get('RABBITMQ_HOST', 'localhost')
        self.__port = os.environ.get('RABBITMQ_PORT', 5672)
        self.__usernamer = os.environ.get('RABBITMQ_USERNAME', 'bugs')
        self.__password = os.environ.get('RABBITMQ_PASSWORD', 'bunny')
        self.__exchange = 'tiktaktoe'
        self.__routing_key = routing_key
        self.__channel = self.__create_channel()

    def __create_channel(self):
        connection_parameters = pika.ConnectionParameters(
            host=self.__host,
            port=self.__port,
            credentials=pika.PlainCredentials(
                username=self.__usernamer, password=self.__password
            ),
        )
        channel = pika.BlockingConnection(connection_parameters).channel()
        channel.exchange_declare(
            exchange=self.__exchange, exchange_type='direct', durable=False
        )
        channel.queue_declare(
            self.__routing_key, arguments={'x-expires': QUEUE_TTL}
        )
        channel.queue_bind(
            self.__routing_key,
            self.__exchange,
            self.__routing_key,
            arguments={'x-expires': QUEUE_TTL},
        )
        return channel

    def send_message(self, body: dict):
        self.__channel.basic_publish(
            exchange=self.__exchange,
            routing_key=self.__routing_key,
            body=json.dumps(body),
            properties=pika.BasicProperties(delivery_mode=2),
        )
