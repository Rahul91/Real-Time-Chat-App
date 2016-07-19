import uuid
from sqlalchemy import Column, String, ForeignKey, \
    UniqueConstraint, and_, Integer
from sqlalchemy.orm import relationship

from healthify.models.channel import Channel
from healthify.models.user import User

from healthify.models.configure import (Model, CREATED_ON_WITH_SERVER_DEFAULT, DELETED_ON, USER_ID_FOREIGN_KEY,
CHANNEL_ID_FOREIGN_KEY, BOOLEAN_FALSE)


__author__ = 'rahul'


class UserChannelMapping(Model):
    __tablename__ = 'user_channel_mapping'

    id = Column(String(36), primary_key=True, default=str(uuid.uuid4()))

    user_id = USER_ID_FOREIGN_KEY.copy()
    channel_id = CHANNEL_ID_FOREIGN_KEY.copy()
    is_unsubscribed = BOOLEAN_FALSE.copy()

    created_on = CREATED_ON_WITH_SERVER_DEFAULT.copy()
    deleted_on = DELETED_ON.copy()

    channel = relationship('Channel')
    user = relationship('User')
