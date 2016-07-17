import uuid
from sqlalchemy import Column, String, ForeignKey, \
    UniqueConstraint, and_, Integer

from healthify.models.configure import (Model, CREATED_ON_WITH_SERVER_DEFAULT, DELETED_ON, USER_ID_FOREIGN_KEY,
CHANNEL_ID_FOREIGN_KEY)


__author__ = 'rahul'


class UserChannelMapping(Model):
    __tablename__ = 'user_channel_mapping'

    id = Column(String(36), primary_key=True, default=str(uuid.uuid4()))

    user_id = USER_ID_FOREIGN_KEY
    channel_id = CHANNEL_ID_FOREIGN_KEY

    created_on = CREATED_ON_WITH_SERVER_DEFAULT.copy()
    deleted_on = DELETED_ON.copy()
