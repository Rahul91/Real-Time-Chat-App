import pika
import json
from uuid import uuid4
from sqlalchemy.exc import SQLAlchemyError
from pika.exceptions import AMQPConnectionError, ConnectionClosed
from flask_restful import abort

from healthify.utils.logger import get_logger
from healthify.models.chat import ChatHistory
from healthify.models.user import User
from healthify.models.channel import Channel
from healthify.models.configure import session
from healthify.config import PIKA_RABBITMQ_HOST, PIKA_RABBITMQ_TYPE, PIKA_RABBITMQ_EXCHANGE

__author__ = 'rahul'

log = get_logger()


class MessageProcessor(object):

    @staticmethod
    def process_messages():
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=PIKA_RABBITMQ_HOST))
            pika_channel = connection.channel()

            pika_channel.exchange_declare(exchange=PIKA_RABBITMQ_EXCHANGE,
                                          type=PIKA_RABBITMQ_TYPE)

            result = pika_channel.queue_declare(exclusive=True)
            queue_name = result.method.queue

            pika_channel.queue_bind(exchange=PIKA_RABBITMQ_EXCHANGE,
                                    queue=queue_name)

            def callback_function(ch, method, properties, body):
                log.info('Message payload: {}'.format(body))
                payload = json.loads(body)
                payload.update(dict(
                    id=str(uuid4()),
                ))

                chat_obj = ChatHistory(**payload)
                session.add(chat_obj)
                session.commit()

            pika_channel.basic_consume(callback_function,
                                       queue=queue_name,
                                       no_ack=True)
            pika_channel.start_consuming()

        except SQLAlchemyError as sa_err:
            log.exception(sa_err)
            session.rollback()
            abort(500, message="API-ERR-DB")
        except ConnectionClosed as pika_exception:
            log.error(repr(pika_exception))
            session.rollback()
            abort(400, message='PIKA-CONNECTION-ERROR')
        except AMQPConnectionError as pika_conn_err:
            log.error(repr(pika_conn_err))
            session.rollback()
            abort(400, message='PIKA-CONNECTION-ERROR')
        except Exception as excp:
            log.error(repr(excp))
            session.rollback()
        finally:
            session.close()


if __name__ == '__main__':
    message_processor = MessageProcessor()
    message_processor.process_messages()
