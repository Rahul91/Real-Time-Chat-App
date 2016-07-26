from flask_jwt import jwt_required, current_identity
from flask_restful import marshal_with, reqparse, fields, abort
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError

from healthify.utils.logger import get_logger
from healthify.functionality.channel import create_channel, get_user_channels, get_channel_by_name, unsubscribe_channel, \
    get_channel_by_id
from healthify.models.configure import session
from healthify.utils.validation import non_empty_str

__author__ = 'rahul'

log = get_logger()


def channel_response_transformation(channel):
    return dict(
        channel_id=channel.id,
        channel_name=channel.name,
        channel_type=channel.type,
        created_by=channel.created_by,
        created_on=str(channel.created_on),
    )


def user_channel_response_transformation(user_channel_mapping):
    channel_obj = get_channel_by_id(channel_id=user_channel_mapping.channel_id)
    return channel_response_transformation(channel_obj)


def channel_unsubscribe_transform_response(channel):
    return dict(
        channel_id=channel.id,
        unsubscribed=True,
    )


class Channel(Resource):
    """
    @api {get} /channel Channel
    @apiName Channel
    @apiGroup Channel
    @apiHeader {String} Authorization

    @apiSuccessExample Success Response
    HTTP/1.1 200 OK
    {
      "created_on": true,
      "created_by": "test",
      "channel_name" : "test_channel",
      "channel_type" : "public",
    }

    @apiErrorExample Invalid Params Provided
    HTTP/1.1 400 Bad Request
    {
      "message": {
        "username": "PUB-INVALID-PARAM"
      }
    }
    """

    decorators = [jwt_required()]

    channel_fetch_response_format = dict(
        channel_name=fields.String,
        channel_type=fields.String,
        created_by=fields.String,
        created_on=fields.String,
    )

    @marshal_with(channel_fetch_response_format)
    def get(self):
        try:
            session.rollback()
            channel_list = get_user_channels(user_id=current_identity.id)
            session.commit()
            return [user_channel_response_transformation(channel) for channel in channel_list] if channel_list else None
        except ValueError as val_err:
            log.error(repr(val_err))
            session.rollback()
            abort(400, message=val_err.message)
        except KeyError as key_err:
            log.error(repr(key_err))
            session.rollback()
            abort(400, message="PUB-INVALID-PARAM")
        except SQLAlchemyError as sa_err:
            log.exception(sa_err)
            session.rollback()
            abort(500, message="API-ERR-DB")
        finally:
            session.close()

    """
    @api {post} /channel/create Create Channel
    @apiName Channel
    @apiGroup Channel

    @apiParam {String} channel_name Channel Name
    @apiParam {String} type Channel type
    @apiHeader {String} Authorization

    @apiSuccessExample Success Response
    HTTP/1.1 200 OK
    {
      "channel_name" : "test_channel",
      "channel_type" : "public",
    }

    @apiErrorExample Channel Name not Provided
    HTTP/1.1 400 Bad Request
    {
      "message": {
        "username": "CHANNEL-REQ-NAME"
      }
    }
    """
    channel_creation_response_format = dict(
        channel_name=fields.String,
        type=fields.String,
    )

    @marshal_with(channel_creation_response_format)
    def post(self):
        create_channel_request_format = reqparse.RequestParser()
        create_channel_request_format.add_argument('channel_name', type=non_empty_str, required=True,
                                                   help="CHANNEL-REQ-NAME")
        create_channel_request_format.add_argument('type', type=non_empty_str, required=False, help="CHANNEL-REQ-TYPE")

        params = create_channel_request_format.parse_args()
        params.update(dict(user_id=current_identity.id))
        log.info('Publish params: {}'.format(params))
        try:
            session.rollback()
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
            abort(400, message="CHANNEL-INVALID-PARAM")
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


class UnsubscribeChannel(Resource):
    """
    @api {post} /channel/unsubscribe Unsubscribe Channel
    @apiName Unsubscribe Channel
    @apiGroup Channel

    @apiParam {String} channel_name Channel Name
    @apiHeader {String} Authorization

    @apiSuccessExample Success Response
    HTTP/1.1 200 OK
    {
      "channel_name" : "test_channel",
      "channel_type" : "public",
    }

    @apiErrorExample Channel Name not Provided
    HTTP/1.1 400 Bad Request
    {
      "message": {
        "username": "CHANNEL-REQ-NAME"
      }
    }
    """
    decorators = [jwt_required()]

    # @marshal_with(channel_creation_response_format)
    def post(self):
        unsubscribe_channel_request_format = reqparse.RequestParser()
        unsubscribe_channel_request_format.add_argument('channel_name', type=non_empty_str, required=True,
                                                        help="CHANNEL-REQ-NAME")

        params = unsubscribe_channel_request_format.parse_args()
        params.update(dict(user_id=current_identity.id))
        log.info('Publish params: {}'.format(params))
        try:
            session.rollback()
            response = unsubscribe_channel(**params)
            session.commit()
            return channel_unsubscribe_transform_response(response)
        except ValueError as val_err:
            log.error(repr(val_err))
            session.rollback()
            abort(400, message=val_err.message)
        except KeyError as key_err:
            log.error(repr(key_err))
            session.rollback()
            abort(400, message="UNSUB-INVALID-PARAM")
        except IOError as io_err:
            log.exception(io_err)
            session.rollback()
            abort(500, message="API-ERR-IO")
        except SQLAlchemyError as sa_err:
            log.exception(sa_err)
            session.rollback()
            abort(500, message="API-ERR-DB")
        except Exception as excp:
            log.error(repr(excp))
            session.rollback()
            abort(400, message=excp.message)
        finally:
            session.close()


class FetchChannel(Resource):
    """
    @api {get} /channel/{channel_name} Fetch Channel
    @apiName Unsubscribe Channel
    @apiGroup Channel

    @apiHeader {String} Authorization

    @apiSuccessExample Success Response
    HTTP/1.1 200 OK
    {
        "channel_id": "channel.id",
        "channel_name": "channel_name",
        "channel_type": "public",
        "created_by": "test_user",
        "created_on": "some date",
    }

    @apiErrorExample Invalid params Provided
    HTTP/1.1 400 Bad Request
    {
      "message": {
        "username": "GET-CHANNEL-INVALID-PARAM"
      }
    }
    """

    def get(self, channel_name):
        try:
            session.rollback()
            response = get_channel_by_name(channel_name=channel_name)
            session.commit()
            return channel_response_transformation(response) if response else None
        except ValueError as val_err:
            log.error(repr(val_err))
            session.rollback()
            abort(400, message=val_err.message)
        except KeyError as key_err:
            log.error(repr(key_err))
            session.rollback()
            abort(400, message="GET-CHANNEL-INVALID-PARAM")
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
