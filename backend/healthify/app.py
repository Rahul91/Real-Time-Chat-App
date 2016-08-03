from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask_cors import CORS

from healthify import config
from healthify.functionality.auth import identity, authenticate
from healthify.utils.logger import get_logger
from healthify.resources.auth import Singup, User, ForgotPassword
from healthify.resources.chat import Chat, MessageStream, FetchChat, DeleteChat
from healthify.resources.channel import Channel, FetchChannel, UnsubscribeChannel, JoinChannelRequest, ApproveJoinRequest

__author__ = 'rahul'

log = get_logger()

app = Flask(config.FLASK_APP_NAME)
app.config.from_object(config)
CORS(app)
api = Api(app)


JWT(app, authenticate, identity)


api.add_resource(Singup, '/signup')
api.add_resource(ForgotPassword, '/password/forgot')
api.add_resource(Chat, '/message/publish')
api.add_resource(DeleteChat, '/message/delete', endpoint='delete_chat')
api.add_resource(FetchChat, '/message')
api.add_resource(MessageStream, '/stream')
api.add_resource(User, '/user')
api.add_resource(Channel, '/channel')
api.add_resource(Channel, '/channel/create', endpoint='save_channel')
api.add_resource(UnsubscribeChannel, '/channel/unsubscribe', endpoint='unsubscribe_channel')
api.add_resource(FetchChannel, '/channel/<string:channel_name>', endpoint='get_channel_details')
api.add_resource(JoinChannelRequest, '/channel/invite')
api.add_resource(JoinChannelRequest, '/channel/pending', endpoint='get_pending_invitation')
api.add_resource(ApproveJoinRequest, '/channel/approve', endpoint='save_user_invitation_response')


# @app.teardown_request
# def close_session(exception):
#     session.close()
#     return exception
#
# app.teardown_appcontext(close_session)

if __name__ == "__main__":
    app.run(debug=config.FLASK_DEBUG, port=config.FLASK_PORT, threaded=True)

