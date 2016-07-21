import pika
import json
from uuid import uuid4

from healthify.utils.logger import get_logger
from healthify.models.chat import ChatHistory
from healthify.models.user import User
from healthify.models.channel import Channel
from healthify.models.configure import session
from healthify.config import PIKA_RABBITMQ_HOST, PIKA_RABBITMQ_TYPE

__author__ = 'rahul'

log = get_logger()


class MessageProcessor(object):

    def process_messages(self, **kwargs):
        channel_name = kwargs.get('channel_name'.replace(" ", "-"), 'public')
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=PIKA_RABBITMQ_HOST))
        pika_channel = connection.channel()

        pika_channel.exchange_declare(exchange=channel_name,
                                      type=PIKA_RABBITMQ_TYPE)

        result = pika_channel.queue_declare(exclusive=True)
        queue_name = result.method.queue

        pika_channel.queue_bind(exchange=channel_name,
                                queue=queue_name)

        def callback_function(ch, method, properties, body):
            print body, type(body)
            payload = json.loads(body)
            payload.update(dict(
                id=str(uuid4()),
            ))

            chat_obj = ChatHistory(**payload)
            session.add(chat_obj)
            session.commit()
            # return message_stream


        pika_channel.basic_consume(callback_function,
                              queue=queue_name,
                              no_ack=True)

        pika_channel.start_consuming()


if __name__ == '__main__':
    message_processor = MessageProcessor()
    message_processor.process_messages()
