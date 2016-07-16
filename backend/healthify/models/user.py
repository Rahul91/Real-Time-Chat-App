import uuid
from sqlalchemy import Column, String, ForeignKey, \
    UniqueConstraint, and_, Integer

from healthify.models.configure import Model, UNIQUE_ID, CREATED_ON_WITH_SERVER_DEFAULT, DELETED_ON

__author__ = 'rahul'


class User(Model):
    __tablename__ = 'user'

    id = Column(String(36), primary_key=True, default=str(uuid.uuid4()))

    username = Column(String(255), unique=True)
    password = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))

    created_on = CREATED_ON_WITH_SERVER_DEFAULT.copy()
    deleted_on = DELETED_ON.copy()
