from flask_jwt import jwt_required, current_identity
from flask_restful import marshal_with, reqparse, fields, abort
from sqlalchemy.exc import SQLAlchemyError

from healthify.models.configure import session
from healthify.utils import logger
from healthify.resources.baseresource import BaseResource as Resource


__author__ = 'rahul'

log = logger.logger


signup_request_format = reqparse.RequestParser()
signup_request_format.add_argument('username', location='form', required=True, help="SUP-REQ-USERNAME")
signup_request_format.add_argument('password', type=basestring, required=True, help="SUP-REQ-PASSWORD")
signup_request_format.add_argument('first_name', type=basestring, required=True, help="SUP-REQ-FIRSTNAME")
signup_request_format.add_argument('last_name', type=basestring, required=True, help="SUP-REQ-LASTNAME")


class Singup(Resource):

    def post(self):
        log.info(self)
        try:
            # response = signup(**params)
            # Create account in sms engine
            # NOTE - Had to call create_account here to avoid circular import
            session.commit()
            # return response
        except ValueError as val_err:
            log.error(repr(val_err))
            session.rollback()
            abort(400, message=val_err.message)
        except KeyError as key_err:
            log.error(repr(key_err))
            session.rollback()
            abort(400, message="SUP-INVALID-PARAM")
        except IOError as io_err:
            log.exception(io_err)
            session.rollback()
            abort(500, message="API-ERR-IO")
        except SQLAlchemyError as sa_err:
            log.exception(sa_err)
            session.rollback()
            abort(500, message="API-ERR-DB")


class Signout(Resource):
    pass


class ForgotPassword(Resource):
    pass

