from flask_jwt import jwt_required, current_identity
from flask_restful import marshal_with, reqparse, fields, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_restful import Resource

from healthify.models.configure import session
from healthify.utils.logger import get_logger
from healthify.functionality.auth import signup, get_user_by_id
from healthify.utils.validation import non_empty_str

__author__ = 'rahul'

log = get_logger()


class Singup(Resource):
    """
    @api {post} /signup User Signup
    @apiName Signup
    @apiGroup User

    @apiParam {String} username Username
    @apiParam {String} password Password
    @apiParam {String} first_name First Name
    @apiParam {String} last_name Last Name

    @apiSuccess {String} username Created user

    @apiSuccessExample Success Response
    HTTP/1.1 200 OK
    {
      "created": true,
      "username": "test@test.com",
      "user_id" : "010c1f06-3971-4e43-bf27-a03b9f5d1e70"
    }

    @apiErrorExample Username is required
    HTTP/1.1 400 Bad Request
    {
      "message": {
        "username": "SIGNUP-REQ-USERNAME"
      }
    }
    @apiErrorExample Username already exists
    HTTP/1.1 400 Bad Request
    {
      "message": {
        "username": "SIGNUP-EXISTS-USERNAME"
      }
    }
    """

    signup_response_format = dict(
        user_id=fields.String,
        username=fields.String,
        created=fields.Boolean,
    )

    @marshal_with(signup_response_format)
    def post(self):
        signup_request_format = reqparse.RequestParser()
        signup_request_format.add_argument('username', type=non_empty_str, required=True, help="SIGNUP-REQ-USERNAME")
        signup_request_format.add_argument('password', type=non_empty_str, required=True, help="SIGNUP-REQ-PASSWORD")
        signup_request_format.add_argument('first_name', type=non_empty_str, required=True, help="SIGNUP-REQ-FIRSTNAME")
        signup_request_format.add_argument('last_name', type=non_empty_str, required=False, help="SIGNUP-REQ-LASTNAME")

        params = signup_request_format.parse_args()
        log.info(params)
        try:
            session.rollback()
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
            abort(400, message="SIGNUP-INVALID-PARAM")
        except IOError as io_err:
            log.exception(io_err)
            session.rollback()
            abort(500, message="API-ERR-IO")
        except SQLAlchemyError as sa_err:
            log.exception(sa_err)
            session.rollback()
            abort(500, message="API-ERR-DB")
        finally:
            session.close()


class User(Resource):
    """
    @api {get} /user User
    @apiName Signup
    @apiGroup User
    @apiHeader {String} Authorization

    @apiSuccessExample Success Response
    HTTP/1.1 200 OK
    {
      "created_on": true,
      "username": "test@test.com",
      "first_name" : "test",
      "last_name" : "test",
    }

    @apiErrorExample Bad Username Provided
    HTTP/1.1 400 Bad Request
    {
      "message": {
        "username": "BAD-USER-ID"
      }
    }
    """

    decorators = [jwt_required()]

    user_response_format = dict(
        username=fields.String,
        first_name=fields.String,
        last_name=fields.String,
        created_on=fields.DateTime,
    )

    @marshal_with(user_response_format)
    def get(self):
        try:
            response = get_user_by_id(user_id=current_identity.id)
            session.commit()
            return dict(
                username=response.username,
                first_name=response.first_name,
                last_name=response.last_name,
                created_on=response.created_on,
            )
        except ValueError as val_err:
            log.error(repr(val_err))
            session.rollback()
            abort(400, message=val_err.message)
        except KeyError as key_err:
            log.error(repr(key_err))
            session.rollback()
            abort(400, message="USR-INVALID-PARAM")
        except IOError as io_err:
            log.exception(io_err)
            session.rollback()
            abort(500, message="API-ERR-IO")
        except SQLAlchemyError as sa_err:
            log.exception(sa_err)
            session.rollback()
            abort(500, message="API-ERR-DB")
        finally:
            session.close()


class ForgotPassword(Resource):
    pass
