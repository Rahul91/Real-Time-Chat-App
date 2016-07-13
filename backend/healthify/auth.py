from healthify.models.configure import session
from healthify.models.user import User

__author__ = 'rahul'


def authenticate(username, password):
    user = session.query(User).filter(User.username == username, User.deleted_on.is_(None)).first()
    if user:
        if user.password == password:
            return user
    return False


def identity(payload):
    return get_user_by_id(user_id=payload['identity'])


def get_user_by_id(**kwargs):
    return session.query(User).filter(User.id == kwargs['user_id'], User.deleted_on.is_(None)).first()