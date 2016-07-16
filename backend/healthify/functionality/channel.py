from models.channel import Channel
from models.configure import session
from utils import validation

__author__ = 'rahul'


@validation.not_empty('channel_name', 'REQ-CHANNEL-NAME', req=True)
@validation.not_empty('user_id', 'REQ-USER-ID', req=True)
@validation.not_empty('type', 'REQ-CHANNEL-TYPE', req=False)
def create_channel(**kwargs):
    channel_type = kwargs.get('channel_type', 'public').lower()
    channel_name = kwargs['channel_name']
    channel_created_by = kwargs['user_id']

    channel_create_params = dict(
        name=channel_name,
        created_by=channel_created_by,
        type=channel_type,
    )
    channel = Channel(**channel_create_params)
    session.add(channel)
    session.flush()

    return dict(
        channel_name=channel.name,
        type=channel.type,
        created=True
    )


@validation.not_empty('channel', 'REQ-CHANNEL-NAME', req=True)
def get_channel_by_name(**kwargs):
    channel =  session.query(Channel).filter(Channel.name == kwargs['channel'], Channel.deleted_on.is_(None))\
        .first()
    if not channel:
        return 'INVALID-CHANNEL-NAME'
    return channel