from flask_jwt import jwt_required, current_identity
from flask_restful import marshal_with, reqparse, fields, abort
from flask_restful import Resource

from healthify.utils import logger
from functionality.channel import create_channel
from healthify.models.configure import session
from healthify.utils.validation import non_empty_str

__author__ = 'rahul'

log = logger.logger


class Channel(Resource):

    decorators = [jwt_required()]

    channel_creation_response_format = dict(
        channel_name=fields.String,
        type=fields.String,
    )

    @marshal_with(channel_creation_response_format)
    def post(self):
        create_channel_request_format = reqparse.RequestParser()
        create_channel_request_format.add_argument('channel_name', type=non_empty_str, required=True, help="CHANNEL-REQ-NAME")
        create_channel_request_format.add_argument('type', type=non_empty_str, required=False, help="CHANNEL-REQ-TYPE")

        params = create_channel_request_format.parse_args()
        params.update(dict(user_id=current_identity.id))
        log.info('Publish params: {}'.format(params))
        try:
            response = create_channel(**params)
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

