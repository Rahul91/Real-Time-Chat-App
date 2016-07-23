from flask_jwt import jwt_required, current_identity
from flask_restful import marshal_with, reqparse, fields, abort
from flask_restful import Resource
from functionality.auth import get_user_by_id
from sqlalchemy.exc import SQLAlchemyError
from pika.exceptions import AMQPConnectionError, ConnectionClosed

from healthify.utils.logger import get_logger
from functionality.chat import publish_message, fetch_message, fetch_stream_messages, delete_chat
from healthify.models.configure import session
from healthify.utils.validation import non_empty_str
from healthify.config import PER_PAGE_RESPONSE_LIMIT

__author__ = 'rahul'

log = get_logger()


class Chat(Resource):
    """
    @api {post} /message/publish Publish/Broadcasts Message
    @apiName Publish Message
    @apiGroup Chat

    @apiParam {String} channel_name
    @apiParam {String} message
    @apiHeader {String} Authorization

    @apiSuccessExample Success Response
    HTTP/1.1 200 OK
    {
        "message_id": "11010f-1344-1345-acf42245",
        "message_published": "True"
    }

    @apiErrorExample Message Payload Missing
    HTTP/1.1 400 Bad Request
    {
      "message": {
        "username": "PUB-REQ-MESSAGE"
      }
    }

    @apiErrorExample Channel NameMissing
    HTTP/1.1 400 Bad Request
    {
      "message": {
        "username": "PUB-REQ-CHANNEL"
      }
    }
    """

    decorators = [jwt_required()]

    message_publish_response_format = dict(
        message_id=fields.String,
        message_published=fields.Boolean,
    )

    @marshal_with(message_publish_response_format)
    def post(self):
        publish_message_request_format = reqparse.RequestParser()
        publish_message_request_format.add_argument('message', type=non_empty_str, required=True, help="PUB-REQ-MESSAGE")
        publish_message_request_format.add_argument('channel_name', type=non_empty_str, required=True, help="PUB-REQ-CHANNEL")

        params = publish_message_request_format.parse_args()
        params.update(dict(user_id=current_identity.id))
        log.info('Publish params: {}'.format(params))
        try:
            session.rollback()
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
        except SQLAlchemyError as sa_err:
            log.exception(sa_err)
            session.rollback()
            abort(500, message="API-ERR-DB")
        except ConnectionClosed as pika_exception:
            log.error(repr(pika_exception))
            session.rollback()
            abort(400, message='PIKA-CONNECTION-ERROR')
        except AMQPConnectionError as pika_conn_err:
            log.error(repr(pika_conn_err))
            session.rollback()
            abort(400, message='PIKA-CONNECTION-ERROR')
        except Exception as excp:
            log.error(repr(excp))
            session.rollback()
        finally:
            session.close()


def message_transformation(message):
    return dict(
        message_id=message.id,
        message_text=message.message,
        published_by_name=message.published_by_name,
        created_on=message.created_on,
    )


class FetchChat(Resource):
    """
    @api {post} /message Fetch Messages
    @apiName Fetch Message
    @apiGroup Chat

    @apiParam {String} channel_name
    @apiParam {String} page_num
    @apiHeader {String} Authorization

    @apiSuccessExample Success Response
    HTTP/1.1 200 OK
    {
        "message_id": "11010f-1344-1345-acf42245",
        "published_by_name": "Rahul",
        "message_text": "THis is a test message",
        "created_on": "2016-10-31"
    }

    @apiErrorExample Page Num Missing
    HTTP/1.1 400 Bad Request
    {
      "message": {
        "username": "MSG-FETCH-REQ-PAGE-NUM"
      }
    }

    @apiErrorExample Channel NameMissing
    HTTP/1.1 400 Bad Request
    {
      "message": {
        "username": "MSG-FETCH-REQ-CHANNEL"
      }
    }
    """

    decorators = [jwt_required()]

    message_response_format = dict(
        message_id=fields.String,
        message_text=fields.String,
        published_by_name=fields.String,
        created_on=fields.DateTime,
    )

    @marshal_with(message_response_format)
    def post(self):

        fetch_message_request_format = reqparse.RequestParser()
        fetch_message_request_format.add_argument('channel_name', type=non_empty_str, required=True, help="MSG-FETCH-REQ-CHANNEL")
        fetch_message_request_format.add_argument('page_num', type=int, required=True, help="MSG-FETCH-REQ-PAGE-NUM")

        params = fetch_message_request_format.parse_args()
        params.update(dict(user_id=current_identity.id))
        params.update(dict(page_size=PER_PAGE_RESPONSE_LIMIT))
        try:
            message_list = []
            session.rollback()
            response = fetch_message(**params)
            session.commit()
            for a_message in response:
                setattr(a_message, 'published_by_name', get_user_by_id(user_id=a_message.published_by).first_name)
                message_list.append(message_transformation(a_message))
            return message_list
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


class DeleteChat(Resource):
    """
    @api {post} /message/delete Delete Messages
    @apiName Delete Message
    @apiGroup Chat

    @apiParam {String} channel_name
    @apiHeader {String} Authorization

    @apiSuccessExample Success Response
    HTTP/1.1 200 OK
    {
        "chat_deleted": True,
    }

    @apiErrorExample Channel NameMissing
    HTTP/1.1 400 Bad Request
    {
      "message": {
        "username": "MSG-DELETE-REQ-CHANNEL"
      }
    }
    """

    decorators = [jwt_required()]

    def post(self):
        delete_chat_params = reqparse.RequestParser()
        delete_chat_params.add_argument('channel_name', type=non_empty_str, required=True,
                                        help="MSG-DELETE-REQ-CHANNEL")

        params = delete_chat_params.parse_args()
        params.update(dict(user_id=current_identity.id))
        try:
            session.rollback()
            response = delete_chat(**params)
            session.commit()
            return response
        except ValueError as val_err:
            log.error(repr(val_err))
            session.rollback()
            abort(400, message=val_err.message)
        except KeyError as key_err:
            log.error(repr(key_err))
            session.rollback()
            abort(400, message="MSG-DELETE-INVALID-PARAM")
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


class MessageStream(Resource):

    # decorators = [jwt_required()]

    message_response_format = dict(
        message_id=fields.String,
        message_text=fields.String,
        published_by_name=fields.String,
        created_on=fields.DateTime,
    )

    @marshal_with(message_response_format)
    def post(self):
        fetch_message_stream_request_format = reqparse.RequestParser()
        fetch_message_stream_request_format.add_argument('channel', type=non_empty_str, required=True, help="MSG-STREAM-REQ-CHANNEL")
        fetch_message_stream_request_format.add_argument('published_by', type=non_empty_str, required=True, help="MSG-STREAM-REQ-PUBLISHER")
        fetch_message_stream_request_format.add_argument('message', type=non_empty_str, required=True, help="MSG-STREAM-REQ-MESSAGE")

        params = fetch_message_stream_request_format.parse_args()
        try:
            session.rollback()
            response = fetch_stream_messages(**params)
            session.commit()
            return response
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
        except SQLAlchemyError as sa_err:
            log.exception(sa_err)
            session.rollback()
            abort(500, message="API-ERR-DB")
        finally:
            session.close()

