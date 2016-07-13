from sqlalchemy import Column, String, ForeignKey, \
    UniqueConstraint, and_, Integer

from healthify.models.configure import Model, UNIQUE_ID, CREATED_ON_WITH_SERVER_DEFAULT, MODIFIED_ON, DELETED_ON

__author__ = 'rahul'


# class Common(Model):
#     id = UNIQUE_ID.copy()
#     created_on = CREATED_ON_WITH_SERVER_DEFAULT.copy()
#     modified_on = MODIFIED_ON.copy()
#     deleted_on = DELETED_ON.copy()


class User(Model):
    __tablename__ = 'user'

    id = UNIQUE_ID.copy()

    username = Column(String(255), unique=True)
    password = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))

    created_on = CREATED_ON_WITH_SERVER_DEFAULT.copy()
    # modified_on = MODIFIED_ON.copy()
    deleted_on = DELETED_ON.copy()
