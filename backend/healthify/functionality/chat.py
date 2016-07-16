import json

from functionality.channel import create_channel, get_channel_by_name
import pika
from healthify.utils import logger
from healthify.config import PIKA_RABBITMQ_HOST, PIKA_RABBITMQ_TYPE
from healthify.models.configure import session
from healthify.models.chat import ChatHistory
from healthify.utils import validation
from healthify.functionality.auth import get_user_by_id

__author__ = 'rahul'

log = logger.logger


@validation.not_empty('message', 'PUB-REQ-MESSAGE-PAYLOAD', req=True)
@validation.not_empty('channel', 'PUB-REQ-CHANNEL', req=True)
def publish_message(**kwargs):
    user = get_user_by_id(user_id=kwargs['user_id'])

    if not get_channel_by_name(channel=kwargs['channel']) and kwargs['channel'] == 'public':
        create_channel(channel_name='public', user_id=kwargs['user_id'], type='public')

    payload = dict(
        published_by=user.id,
        message=kwargs['message'],
        channel=get_channel_by_name(channel=kwargs['channel']).id,
    )

    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=PIKA_RABBITMQ_HOST))
    pika_channel = connection.channel()
    pika_channel.exchange_declare(exchange=kwargs['channel'].replace(" ", "-"),
                                  type=PIKA_RABBITMQ_TYPE)

    pika_channel.basic_publish(exchange=kwargs['channel'],
                               routing_key='',
                               body=json.dumps(payload))
    connection.close()

    chat_obj = ChatHistory(**payload)
    session.add(chat_obj)
    session.flush()

    return dict(
        message_id=chat_obj.id,
        message_published=True
    )


@validation.not_empty('user_id', 'REQ-USER-ID', req=True)
def fetch_message(**kwargs):
    # user = get_user_by_id(user_id=kwargs['user_id'])
    message_list = session.query(ChatHistory).filter(ChatHistory.deleted_on.is_(None)).all()
    return message_list
