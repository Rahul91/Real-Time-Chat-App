import json
from uuid import uuid4
from datetime import datetime
from sqlalchemy import desc
import pika

from functionality.channel import create_channel, get_channel_by_name, is_channel_unsubscribed, get_channel_by_id
from healthify.utils.logger import get_logger
from healthify.config import PIKA_RABBITMQ_HOST, PIKA_RABBITMQ_TYPE, PIKA_RABBITMQ_EXCHANGE
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

    payload = dict(
        published_by=user.id,
        message=kwargs['message'],
        channel=get_channel_by_name(channel_name=kwargs['channel_name']).id,
        created_on=str(datetime.now()),
    )

    connection = pika.BlockingConnection(pika.ConnectionParameters(host=PIKA_RABBITMQ_HOST))
    pika_channel = connection.channel()
    pika_channel.exchange_declare(exchange=PIKA_RABBITMQ_EXCHANGE,
                                  type=PIKA_RABBITMQ_TYPE)

    pika_channel.basic_publish(exchange=PIKA_RABBITMQ_EXCHANGE,
                               routing_key='',
                               body=json.dumps(payload))
    connection.close()

    # payload.update(dict(
    #      id=str(uuid4()),
    # ))
    # chat_obj = ChatHistory(**payload)
    # session.add(chat_obj)
    # session.flush()

    return dict(
        message_published=True
    )


@validation.not_empty('user_id', 'REQ-USER-ID', req=True)
@validation.not_empty('channel_name', 'REQ-CHANNEL-NAME', req=True)
@validation.not_empty('page_size', 'REQ-PAGE-SIZE', req=True, var_type=int)
@validation.not_empty('page_num', 'REQ-PAGE-NUM', req=True, var_type=int)
def fetch_message(**kwargs):
    message_list = []
    user_id = kwargs['user_id']
    channel_obj = get_channel_by_name(channel_name=kwargs['channel_name'])
    if not is_channel_unsubscribed(channel_id=channel_obj.id, user_id=user_id):
        page_size = kwargs['page_size']
        page = kwargs['page_num']
        message_list = session.query(ChatHistory) \
            .filter(ChatHistory.channel == channel_obj.id, ChatHistory.deleted_on.is_(None)) \
            .order_by(desc(ChatHistory.created_on))
        if page_size:
            message_list = message_list.limit(10)
        if page:
            message_list = message_list.offset(page*page_size)
        message_marked_deleted = chat_marked_deleted(user_id=user_id, channel_id=channel_obj.id)
        if message_marked_deleted[0]:
            message_list = [message_list for message in message_list.all()
                            if message.created_on > message_marked_deleted[0]][0]
        if message_list:
            return message_list.all()
        else:
            return message_list

    return message_list


@validation.not_empty('user_id', 'REQ-USER-ID', req=True)
@validation.not_empty('channel_id', 'REQ-CHANNEL-ID', req=True)
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
    channel = get_channel_by_name(channel_name=kwargs['channel_name'])
    chat_obj = session.query(UserChannelMapping) \
        .filter(UserChannelMapping.user_id == kwargs['user_id'], UserChannelMapping.channel_id == channel.id)\
        .first()
    setattr(chat_obj, 'deleted_on', datetime.now())
    session.add(chat_obj)
    return dict(
        chat_deleted=True,
    )

@validation.not_empty('user_id', 'REQ-USER-ID', req=True)
@validation.not_empty('channel_id', 'REQ-CHANNEL-ID', req=True)
def chat_marked_deleted(**kwargs):
    return session.query(UserChannelMapping.deleted_on).\
        filter(UserChannelMapping.user_id==kwargs['user_id']).\
        filter(UserChannelMapping.channel_id==kwargs['channel_id']).first()
