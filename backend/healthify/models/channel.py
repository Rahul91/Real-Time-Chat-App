import uuid
from sqlalchemy import Column, String, ForeignKey, \
    UniqueConstraint, and_, Integer, Enum

from healthify.models.configure import (Model, CREATED_ON_WITH_SERVER_DEFAULT, TIMESTAMP,
                                        DELETED_ON, NAME_NULLABLE_FALSE, USER_ID_FOREIGN_KEY, CHANNEL_ID_FOREIGN_KEY)

__author__ = 'rahul'


class Channel(Model):
    __tablename__ = 'channel'

    id = Column(String(36), primary_key=True, default=str(uuid.uuid4()))

    name = NAME_NULLABLE_FALSE.copy()
    created_by = USER_ID_FOREIGN_KEY.copy()
    type = Column(Enum('private', 'public', name='channel_types'))

    created_on = CREATED_ON_WITH_SERVER_DEFAULT.copy()
    deleted_on = DELETED_ON.copy()


class ChannelJoinRequest(Model):
    __tablename__ = 'channel_join_request'

    id = Column(String(36), primary_key=True, default=str(uuid.uuid4()))

    requested_by = USER_ID_FOREIGN_KEY.copy()
    requested_for = Column(String(63), nullable=False)
    channel_id = CHANNEL_ID_FOREIGN_KEY.copy()
    accepted_on = TIMESTAMP.copy()
    rejected_on = TIMESTAMP.copy()

    created_on = CREATED_ON_WITH_SERVER_DEFAULT.copy()
    deleted_on = DELETED_ON.copy()