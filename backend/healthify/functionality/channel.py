from uuid import uuid4

from healthify.models.chat import ChatHistory
from healthify.models.common import UserChannelMapping
from healthify.utils.logger import get_logger
from healthify.models.channel import Channel
from healthify.models.user import User
from healthify.models.common import UserChannelMapping
from healthify.models.configure import session
from utils import validation

__author__ = 'rahul'

log = get_logger()


@validation.not_empty('channel_name', 'REQ-CHANNEL-NAME', req=True)
@validation.not_empty('user_id', 'REQ-USER-ID', req=True)
@validation.not_empty('type', 'REQ-CHANNEL-TYPE', req=False)
def create_channel(**kwargs):
    channel_name = kwargs['channel_name']
    user_id = kwargs['user_id']
    channel_obj = get_channel_by_name(channel_name=channel_name)
    channel_type = kwargs.get('channel_type', 'public').lower()
    if not channel_obj:
        channel_create_params = dict(
            id=str(uuid4()),
            name=channel_name,
            created_by=user_id,
            type=channel_type,
        )
        channel = Channel(**channel_create_params)
        session.add(channel)

        create_user_channel_mapping(user_id=user_id,
                                    channel_id=get_channel_by_name(channel_name=channel_name).id)
    else:
        create_user_channel_mapping(user_id=user_id,
                                    channel_id=get_channel_by_name(channel_name=channel_name).id)
    return dict(
        channel_name=channel_name,
        type=channel_type,
        created=True
    )


@validation.not_empty('channel_name', 'REQ-CHANNEL-NAME', req=True)
def get_channel_by_name(**kwargs):
    channel = session.query(Channel).filter(Channel.name == kwargs['channel_name'], Channel.deleted_on.is_(None))\
        .first()
    if not channel:
        raise ValueError('INVALID-CHANNEL-NAME')
    return channel


@validation.not_empty('user_id', 'REQ-USER-ID', req=True)
def get_user_channels(**kwargs):
    channel = session.query(UserChannelMapping).\
        filter(UserChannelMapping.user_id == kwargs['user_id'], UserChannelMapping.is_unsubscribed == False).\
        all()
    return [get_channel_by_id(channel_id=a_channel.channel_id) for a_channel in channel]


@validation.not_empty('user_id', 'REQ-USER-ID', req=True)
@validation.not_empty('channel_id', 'REQ-CHANNEL-ID', req=True)
def create_user_channel_mapping(**kwargs):
    params = dict(
        id=str(uuid4()),
        user_id=kwargs['user_id'],
        channel_id=kwargs['channel_id'],
    )
    user_channel_mapping = UserChannelMapping(**params)
    session.add(user_channel_mapping)
    return user_channel_mapping


@validation.not_empty('channel_id', 'REQ-CHANNEL-ID', req=True)
@validation.not_empty('user_id', 'REQ-USER-ID', req=True)
def is_channel_unsubscribed(**kwargs):
    channel_mapping = session.query(UserChannelMapping)\
        .filter(UserChannelMapping.user_id == kwargs['user_id'], UserChannelMapping.channel_id == kwargs['channel_id'])\
        .first()
    if not channel_mapping:
        channel_mapping = create_user_channel_mapping(user_id=kwargs['user_id'], channel_id=kwargs['channel_id'])
    if channel_mapping and channel_mapping.is_unsubscribed:
        return True
    return False


@validation.not_empty('channel_id', 'REQ-CHANNEL-ID', req=True)
def get_channel_by_id(**kwargs):
    channel = session.query(Channel).filter(Channel.id == kwargs['channel_id'], Channel.deleted_on.is_(None))\
        .first()
    if not channel:
        raise ValueError('INVALID-CHANNEL-ID')
    return channel


@validation.not_empty('channel_name', 'REQ-CHANNEL-NAME', req=True)
@validation.not_empty('user_id', 'REQ-USER-ID', req=True)
def unsubscribe_channel(**kwargs):
    channel = get_channel_by_name(channel_name=kwargs['channel_name'])
    user_id = kwargs['user_id']

    user_channel_obj = session.query(UserChannelMapping)\
        .filter(UserChannelMapping.user_id == user_id,
                UserChannelMapping.channel_id == channel.id, UserChannelMapping.deleted_on.is_(None))\
        .first()
    if not user_channel_obj:
        raise ValueError('INVALID-CHANNEL-MAPPING')
    else:
        setattr(user_channel_obj, 'is_unsubscribed', True)
        session.add(user_channel_obj)
        return user_channel_obj
