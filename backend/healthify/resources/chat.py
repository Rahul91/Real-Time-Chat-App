from flask_jwt import jwt_required, current_identity
from flask_restful import marshal_with, reqparse, fields, abort
from flask_restful import Resource
from functionality.auth import get_user_by_id
from sqlalchemy.exc import SQLAlchemyError

from healthify.utils import logger
from functionality.chat import publish_message, fetch_message
from healthify.models.configure import session
from healthify.utils.validation import non_empty_str

__author__ = 'rahul'

log = logger.logger


class Publish(Resource):

    decorators = [jwt_required()]

    message_publish_response_format = dict(
        message_id=fields.String,
        published=fields.Boolean,
    )

    @marshal_with(message_publish_response_format)
    def post(self):
        publish_message_request_format = reqparse.RequestParser()
        publish_message_request_format.add_argument('message', type=non_empty_str, required=True, help="PUB-REQ-MESSAGE")
        publish_message_request_format.add_argument('channel', type=non_empty_str, required=True, help="PUB-REQ-CHANNEL")

        params = publish_message_request_format.parse_args()
        params.update(dict(user_id=current_identity.id))
        log.info('Publish params: {}'.format(params))
        try:
            response = publish_message(**params)
            session.commit()
            return response
        except ValueError as val_err:
            log.error(repr(val_err))
            session.rollback()
            abort(400, message=val_err.message)
        except KeyError as key_err:
            log.error(repr(key_err))
            session.rollback()
            abort(400, message="PUB-INVALID-PARAM")
        except IOError as io_err:
            log.exception(io_err)
            session.rollback()
            abort(500, message="API-ERR-IO")
        # except SQLAlchemyError as sa_err:
        #     log.exception(sa_err)
        #     session.rollback()
        #     abort(500, message="API-ERR-DB")
        except Exception as e:
            print e
            session.rollback()


def message_transformation(message):
    return dict(
        message_id=message.id,
        message_text=message.message,
        published_by=message.published_by,
        created_on=message.created_on,
    )


class Fetch(Resource):

    decorators = [jwt_required()]

    message_response_format = dict(
        message_id=fields.String,
        message_text=fields.String,
        published_by=fields.String,
        created_on=fields.DateTime,
    )

    @marshal_with(message_response_format)
    def get(self):
        try:
            response = fetch_message(user_id=current_identity.id)
            session.commit()
            for a_message in response:
                a_message.published_by = get_user_by_id(user_id=a_message.published_by).first_name
            return [message_transformation(a_message) for a_message in response]
        except ValueError as val_err:
            log.error(repr(val_err))
            session.rollback()
            abort(400, message=val_err.message)
        except KeyError as key_err:
            log.error(repr(key_err))
            session.rollback()
            abort(400, message="MSG-INVALID-PARAM")
        except IOError as io_err:
            log.exception(io_err)
            session.rollback()
            abort(500, message="API-ERR-IO")
        # except SQLAlchemyError as sa_err:
        #     log.exception(sa_err)
        #     session.rollback()
        #     abort(500, message="API-ERR-DB")
        except Exception as e:
            print e
            session.rollback()