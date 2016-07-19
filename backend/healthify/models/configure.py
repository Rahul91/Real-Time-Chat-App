from uuid import uuid1
from datetime import datetime
from sqlalchemy import (
    orm, create_engine, Column, String, ForeignKey, DateTime, TIMESTAMP, text, Integer
)
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.declarative import declarative_base

from healthify.config import (SQLALCHEMY_DATABASE_URI, SQLALCHEMY_CONVERT_UNICODE, SQLALCHEMY_POOL_CYCLE, SQLALCHEMY_ECHO)
__author__ = 'rahul'

Model = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URI,
                       convert_unicode=SQLALCHEMY_CONVERT_UNICODE,
                       pool_recycle=SQLALCHEMY_POOL_CYCLE,
                       echo=SQLALCHEMY_ECHO)

# Why pool_recycle : http://docs.sqlalchemy.org/en/rel_0_9/dialects/mysql.html#connection-timeouts
_Session = orm.sessionmaker(autocommit=False, autoflush=True, bind=engine, expire_on_commit=False)
session = orm.scoped_session(_Session)
# session = _Session()
Model.metadata.bind = engine
Model.query = session.query_property()

UNIQUE_ID = Column(String(36), primary_key=True, default=str(uuid1()))
CREATED_ON = Column(DateTime, default=datetime.now())
CREATED_ON_WITH_SERVER_DEFAULT = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
MODIFIED_ON = Column(TIMESTAMP, nullable=False, default=datetime.now(),
                     server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
DELETED_ON = Column(DateTime)

BOOLEAN_TRUE = Column(TINYINT(1), default=1, nullable=False)
BOOLEAN_FALSE = Column(TINYINT(1), default=0, nullable=False)


NAME = Column(String(255), unique=True)
NAME_NULLABLE_FALSE = Column(String(255), unique=True, nullable=False)
AUTO_INCREMENTAL_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

USER_ID_FOREIGN_KEY = Column(String(36), ForeignKey('user.id'))
CHANNEL_ID_FOREIGN_KEY = Column(String(36), ForeignKey('channel.id'))
MESSAGE_ID_FOREIGN_KEY = Column(String(36), ForeignKey('message.id'))


