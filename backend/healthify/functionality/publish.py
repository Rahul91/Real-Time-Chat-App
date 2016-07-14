import pika
import sys

from healthify.utils import logger
from healthify.config import PIKA_RABBITMQ_EXCHANGE, PIKA_RABBITMQ_HOST, PIKA_RABBITMQ_TYPE
from healthify.models.configure import session
from healthify.models.channel import Channel
from healthify.utils import validation
from healthify.functionality.auth import get_user_by_id

__author__ = 'rahul'

log = logger.logger


@validation.not_empty('payload', 'PUB-REQ-MESSAGE-PAYLOAD', req=True)
def publish_message(**kwargs):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=PIKA_RABBITMQ_HOST))
    channel = connection.channel()
    channel.exchange_declare(exchange=PIKA_RABBITMQ_EXCHANGE,
                             type=PIKA_RABBITMQ_TYPE)

    user = get_user_by_id(user_id=kwargs['user_id'])
    payload = kwargs['payload']

    if not get_channel_by_name(channel=kwargs['channel']):
        create_channel(user_id=user.id, channel_name=channel)

    channel.basic_publish(exchange=PIKA_RABBITMQ_EXCHANGE,
                          routing_key='',
                          body=payload)

    connection.close()
    return dict(
        message_published=True
    )


@validation.not_empty('channel', 'REQ-CHANNEL-NAME', req=True)
def get_channel_by_name(**kwargs):
    return session.query(Channel).filter(Channel.name == kwargs['channel'], Channel.deleted_on.is_(None))\
        .first()


@validation.not_empty('channel_name', 'REQ-CHANNEL-NAME', req=True)
@validation.not_empty('user_id', 'REQ-USER-ID', req=True)
@validation.not_empty('type', 'REQ-CHANNEL-TYPE', req=False)
def create_channel(**kwargs):
    channel_type = kwargs.get('channel_type', 'public')
    channel_name = kwargs['name']
    channel_created_by = get_user_by_id(user_id=kwargs['user_id']).username

    channel_create_params = dict(
        name=channel_name,
        created_by=channel_created_by,
        type=channel_type,
    )
    channel = Channel(**channel_create_params)
    session.add(channel)
    return dict(
        channel_name=channel.name,
        created=True
    )