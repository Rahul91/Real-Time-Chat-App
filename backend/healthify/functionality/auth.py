from functools import wraps
from flask import request, jsonify
from flask_jwt import jwt_required, JWT
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

from healthify.models.configure import session
from healthify.models.user import User
from healthify.utils import validation
from healthify.utils import logger

log = logger.logger

__author__ = 'rahul'


@validation.valid_username('username', 'SIGNUP-BAD-USERNAME')
@validation.not_empty('first_name', 'SIGNUP-REQ-FIRSTNAME', req=True)
@validation.not_empty('last_name', 'SIGNUP-REQ-LASTNAME', req=True)
def signup(**kwargs):
    if not get_user_by_username(username=kwargs['username']):
        user = User(**kwargs)
        session.add(user)
        session.flush()
        log.info("User added. id=%s", user.id)
    else:
        raise ValueError('SIGNUP-EXISTS-USERNAME')
    return dict(
        user_id=user.id,
        username=user.username,
        created=True
    )


@validation.not_empty('username', 'REQ-USERNAME', req=True)
def get_user_by_username(**kwargs):
    log.info('In get_user_by_username')
    return session.query(User) \
        .filter(User.username == kwargs['username'], User.deleted_on.is_(None)) \
        .first()


def authenticate(username, password):
    user = session.query(User).filter(User.username == username, User.deleted_on.is_(None)).first()
    if user:
        if user.password == password:
            return user
    return False


def identity(payload):
    return get_user_by_id(user_id=payload['identity'])


@validation.not_empty('user_id', 'REQ-USER-ID', req=True)
def get_user_by_id(**kwargs):
    user = session.query(User).filter(User.id == kwargs['user_id'], User.deleted_on.is_(None)).first()
    if not user:
        raise ValueError('BAD-USER-ID')
    return user
