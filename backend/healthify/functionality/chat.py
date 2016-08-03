import json
from uuid import uuid4
from datetime import datetime
from sqlalchemy import desc
import pika
from zmq import green as zmq
# from flask import Response

from healthify.functionality.channel import (create_channel, get_channel_by_name,
                                             is_channel_unsubscribed, get_channel_by_id)
from healthify.utils.logger import get_logger
from healthify.config import PIKA_RABBITMQ_HOST, PIKA_RABBITMQ_TYPE, PIKA_RABBITMQ_EXCHANGE, PER_PAGE_RESPONSE_LIMIT
from healthify.models.configure import session
from healthify.models.chat import ChatHistory
from healthify.models.common import UserChannelMapping
from healthify.models.user import User
from healthify.utils import validation
from healthify.functionality.auth import get_user_by_id
# from healthify.worker.stream_fetch import MessageProcessor
# from healthify.worker.stream_fetch import message_list

__author__ = 'rahul'

log = get_logger()

ctx = zmq.Context()
pubsock = ctx.socket(zmq.PUB)
pubsock.bind('inproc://pub')


@validation.not_empty('message', 'PUB-REQ-MESSAGE-PAYLOAD', req=True)
@validation.not_empty('channel_name', 'PUB-REQ-CHANNEL', req=True)
@validation.not_empty('user_id', 'REQ-USER-ID', req=True)
def publish_message(**kwargs):
    log.info('Publish Message kwargs: {}'.format(kwargs))

    user = get_user_by_id(user_id=kwargs['user_id'])
    payload = dict(
        published_by=user.id,
        message=kwargs['message'],
        channel=get_channel_by_name(channel_name=kwargs['channel_name']).id,
        created_on=str(datetime.now()),
    )
    
    # Comment the following part upto conneciton.close(), to make the process sync
    # And uncomment the below commented part, so that db call is done here and not in pika worker.
    
    # connection = pika.BlockingConnection(pika.ConnectionParameters(host=PIKA_RABBITMQ_HOST))
    # pika_channel = connection.channel()
    # pika_channel.exchange_declare(exchange=PIKA_RABBITMQ_EXCHANGE,
    #                               type=PIKA_RABBITMQ_TYPE)
    #
    # pika_channel.basic_publish(exchange=PIKA_RABBITMQ_EXCHANGE,
    #                            routing_key='',
    #                            body=json.dumps(payload))
    # connection.close()
    global pubsock
    pubsock.send_json(payload)

    payload.update(dict(
        id=str(uuid4()),
    ))
    chat_obj = ChatHistory(**payload)
    session.add(chat_obj)
    session.flush()

    return dict(
        message_published=True
    )


@validation.not_empty('user_id', 'REQ-USER-ID', req=True)
@validation.not_empty('channel_name', 'REQ-CHANNEL-NAME', req=True)
@validation.not_empty('page_size', 'REQ-PAGE-SIZE', req=True, var_type=int)
@validation.not_empty('page_num', 'REQ-PAGE-NUM', req=True, var_type=int)
def fetch_message(**kwargs):
    log.info('Fetch Message kwargs: {}'.format(kwargs))
    message_list = []
    user_id = kwargs['user_id']
    channel_obj = get_channel_by_name(channel_name=kwargs['channel_name'])
    if channel_obj and not is_channel_unsubscribed(channel_id=channel_obj.id, user_id=user_id):
        page_size = kwargs['page_size']
        page = kwargs['page_num']
        message_list = session.query(ChatHistory) \
            .filter(ChatHistory.channel == channel_obj.id, ChatHistory.deleted_on.is_(None)) \
            .order_by(desc(ChatHistory.created_on))
        if page_size:
            message_list = message_list.limit(PER_PAGE_RESPONSE_LIMIT)
        if page:
            message_list = message_list.offset(page*page_size)
        message_marked_deleted = chat_marked_deleted(user_id=user_id, channel_id=channel_obj.id)
        if not message_marked_deleted[0]:
            return message_list.all()
        else:
            return [message for message in message_list.all()
                    if message.created_on > message_marked_deleted[0]]

    return message_list


# @validation.not_empty('user_id', 'REQ-USER-ID', req=True)
# @validation.not_empty('channel_id', 'REQ-CHANNEL-ID', req=True)
def fetch_stream_messages(**kwargs):
    log.info('Fetch Message Stream kwargs: {}'.format(kwargs))
    subsock = ctx.socket(zmq.SUB)
    subsock.setsockopt(zmq.SUBSCRIBE, '')
    subsock.connect('inproc://pub')
    message_stream = subsock.recv_json()
    log.info('Fetch Message Stream kwargs: {}'.format(message_stream))
    # if json.loads(message_stream).channel
    return message_stream


def fetch_stream(**kwargs):
    channel_obj = get_channel_by_name(channel_name=kwargs['channel_name'])
    return session.query(ChatHistory)\
        .filter(ChatHistory.channel == channel_obj.id, ChatHistory.deleted_on.is_(None)) \
        .order_by(desc(ChatHistory.created_on))


@validation.not_empty('user_id', 'REQ-USER-ID', req=True)
@validation.not_empty('channel_name', 'REQ-CHANNEL-NAME', req=True)
def delete_chat(**kwargs):
    log.info('Delete chat kwargs: {}'.format(kwargs))
    channel = get_channel_by_name(channel_name=kwargs['channel_name'])
    chat_obj = session.query(UserChannelMapping) \
        .filter(UserChannelMapping.user_id == kwargs['user_id'], UserChannelMapping.channel_id == channel.id)\
        .first()
    setattr(chat_obj, 'marked_deleted_on', datetime.now())
    session.add(chat_obj)
    return dict(
        chat_deleted=True,
    )


@validation.not_empty('user_id', 'REQ-USER-ID', req=True)
@validation.not_empty('channel_id', 'REQ-CHANNEL-ID', req=True)
def chat_marked_deleted(**kwargs):
    return session.query(UserChannelMapping.marked_deleted_on).\
        filter(UserChannelMapping.user_id==kwargs['user_id']).\
        filter(UserChannelMapping.channel_id==kwargs['channel_id']).first()
