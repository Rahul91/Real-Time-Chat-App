from flask_jwt import jwt_required, current_identity
from flask_restful import marshal_with, reqparse, fields, abort
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError

from healthify.utils import logger
from functionality.publish import publish_message
from healthify.models.configure import session
from healthify.utils.validation import non_empty_str
from healthify.config import PIKA_RABBITMQ_EXCHANGE, PIKA_RABBITMQ_HOST, PIKA_RABBITMQ_TYPE

__author__ = 'rahul'

log = logger.logger


class Publish(Resource):

    decorators = [jwt_required()]

    def post(self):
        publish_message_request_format = reqparse.RequestParser()
        publish_message_request_format.add_argument('payload', type=non_empty_str, required=True, help="PUB-REQ-PAYLOAD")
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
            abort(400, message="SUP-INVALID-PARAM")
        except IOError as io_err:
            log.exception(io_err)
            session.rollback()
            abort(500, message="API-ERR-IO")
        except SQLAlchemyError as sa_err:
            log.exception(sa_err)
            session.rollback()
            abort(500, message="API-ERR-DB")


