from flask_jwt import jwt_required, current_identity
from flask_restful import marshal_with, reqparse, fields, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_restful import Resource

from healthify.models.configure import session
from healthify.utils import logger
from healthify.functionality.auth import signup
from healthify.utils.validation import non_empty_str

signup_response_format = dict(
    user_id=fields.String,
    username=fields.String,
    created=fields.Boolean,
)

__author__ = 'rahul'

log = logger.logger


class Singup(Resource):

    @marshal_with(signup_response_format)
    def post(self):
        signup_request_format = reqparse.RequestParser()
        signup_request_format.add_argument('username', type=non_empty_str, required=True, help="SUP-REQ-USERNAME")
        signup_request_format.add_argument('password', type=non_empty_str, required=True, help="SUP-REQ-PASSWORD")
        signup_request_format.add_argument('first_name', type=non_empty_str, required=True, help="SUP-REQ-FIRSTNAME")
        signup_request_format.add_argument('last_name', type=non_empty_str, required=True, help="SUP-REQ-LASTNAME")

        params = signup_request_format.parse_args()
        log.info(params)
        try:
            response = signup(**params)
            session.commit()
            return response
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

