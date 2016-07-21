from uuid import uuid4

from healthify.models.configure import session
from healthify.models.user import User
from healthify.utils import validation
from healthify.utils.logger import get_logger

log = get_logger()

__author__ = 'rahul'


@validation.valid_username('username', 'SIGNUP-BAD-USERNAME')
@validation.not_empty('first_name', 'SIGNUP-REQ-FIRSTNAME', req=True)
@validation.not_empty('last_name', 'SIGNUP-REQ-LASTNAME', req=True)
def signup(**kwargs):
    if not get_user_by_username(username=kwargs['username']):
        kwargs.update(dict(
            id=str(uuid4()),
        ))
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
    """
    @api {post} /auth Authentication
    @apiName Authentication/Login
    @apiGroup User

    @apiHeader {String} Content-Type Should be application/json for /auth
    @apiParam {String} username Username of the user
    @apiParam {String} password Password of the user

    @apiSuccess {String} access_code JWT

    @apiSuccessExample Success Response
    HTTP/1.1 200 OK
    {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6IjM5MDA4MGExLWY0ZjctMTFlNS04NTRkLTI4ZDI0NDQyZDNlNyIsImlhdCI6MTQ1OTE3ODE0NSwibmJmIjoxNDU5MTc4MTQ1LCJleHAiOjE0NTkxNzg0NDV9.nx_1a4RmvJ7Vlf1CvnMzqoTfzChcuJnDb1Tjy1_FnXw"
    }

    @apiErrorExample Invalid Credentials
    {
      "description": "Invalid credentials",
      "error": "Bad Request",
      "status_code": 401
    }
    """
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
