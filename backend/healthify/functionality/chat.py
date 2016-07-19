import json
from uuid import uuid4
from datetime import datetime
from sqlalchemy import desc
import pika

from functionality.channel import create_channel, get_channel_by_name, get_channel_by_id, is_channel_unsubscribed
from healthify.utils.logger import get_logger
from healthify.config import PIKA_RABBITMQ_HOST, PIKA_RABBITMQ_TYPE
from healthify.models.configure import session
from healthify.models.chat import ChatHistory
from healthify.models.common import UserChannelMapping
from healthify.models.user import User
from healthify.utils import validation
from healthify.functionality.auth import get_user_by_id

__author__ = 'rahul'

log = get_logger()


@validation.not_empty('message', 'PUB-REQ-MESSAGE-PAYLOAD', req=True)
@validation.not_empty('channel_name', 'PUB-REQ-CHANNEL', req=True)
def publish_message(**kwargs):
    user = get_user_by_id(user_id=kwargs['user_id'])

    if not get_channel_by_name(channel=kwargs['channel_name']) and kwargs['channel'] == 'public':
        create_channel(channel_name='public', user_id=kwargs['user_id'], type='public')

    payload = dict(
        published_by=user.id,
        message=kwargs['message'],
        channel=get_channel_by_name(channel=kwargs['channel_name']).id,
        created_on=str(datetime.now()),
    )

    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=PIKA_RABBITMQ_HOST))
    pika_channel = connection.channel()
    pika_channel.exchange_declare(exchange=kwargs['channel_name'].replace(" ", "-"),
                                  type=PIKA_RABBITMQ_TYPE)

    pika_channel.basic_publish(exchange=kwargs['channel_name'],
                               routing_key='',
                               body=json.dumps(payload))
    connection.close()

    payload.update(dict(
         id=str(uuid4()),
    ))
    chat_obj = ChatHistory(**payload)
    session.add(chat_obj)
    session.flush()

    return dict(
        message_id=chat_obj.id,
        message_published=True
    )


@validation.not_empty('user_id', 'REQ-USER-ID', req=True)
@validation.not_empty('channel_name', 'REQ-CHANNEL-NAME', req=True)
@validation.not_empty('page_size', 'REQ-PAGE-SIZE', req=True, var_type=int)
@validation.not_empty('page_num', 'REQ-PAGE-NUM', req=True, var_type=int)
def fetch_message(**kwargs):
    message_list = []
    user_id = kwargs['user_id']
    channel_obj = get_channel_by_name(channel=kwargs['channel_name'])
    if not is_channel_unsubscribed(channel_id=channel_obj.id, user_id=user_id):
        page_size = kwargs['page_size']
        page = kwargs['page_num']
        message_list = session.query(ChatHistory, UserChannelMapping) \
            .filter(ChatHistory.channel == channel_obj.id, ChatHistory.deleted_on.is_(None)) \
            .filter(UserChannelMapping.is_unsubscribed is True) \
            .order_by(desc(ChatHistory.created_on))
        if page_size:
            message_list = message_list.limit(10)
        if page:
            message_list = message_list.offset(page*page_size)
        return message_list.all()

    return message_list


@validation.not_empty('user_id', 'REQ-USER-ID', req=True)
@validation.not_empty('channel_name', 'REQ-CHANNEL-ID', req=True)
def fetch_stream_messages(**kwargs):
    return dict(
        message=kwargs['message'],
        channel=get_channel_by_id(channel_id=kwargs['channel']),
        published_by_name=get_user_by_id(user_id=kwargs['published_by']).first_name,
        created_on=datetime.now(),
    )


@validation.not_empty('user_id', 'REQ-USER-ID', req=True)
@validation.not_empty('channel_name', 'REQ-CHANNEL-NAME', req=True)
def delete_chat(**kwargs):
    channel = get_channel_by_name(channel=kwargs['channel_name'])
    chat_obj = session.query(UserChannelMapping) \
        .filter(UserChannelMapping.user_id == kwargs['user_id'], UserChannelMapping.channel_id == channel.id)\
        .first()
    setattr(chat_obj, 'deleted_on', datetime.now())
    session.add(chat_obj)
    return dict(
        chat_deleted=True,
    )