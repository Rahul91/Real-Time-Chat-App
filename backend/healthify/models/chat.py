import uuid
from sqlalchemy import Column, String, ForeignKey, \
    UniqueConstraint, and_, Integer, Enum

from healthify.models.configure import (Model, UNIQUE_ID, CREATED_ON_WITH_SERVER_DEFAULT,
                                        DELETED_ON, NAME_NULLABLE_FALSE, USER_ID_FOREIGN_KEY, CHANNEL_ID_FOREIGN_KEY)

__author__ = 'rahul'


class ChatHistory(Model):
    __tablename__ = 'chat_history'

    id = Column(String(36), primary_key=True, default=str(uuid.uuid4()))

    message = Column(String(4096))
    published_by = USER_ID_FOREIGN_KEY.copy()
    channel = CHANNEL_ID_FOREIGN_KEY.copy()

    created_on = CREATED_ON_WITH_SERVER_DEFAULT.copy()
    deleted_on = DELETED_ON.copy()