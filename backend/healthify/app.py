import json

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT, jwt_required, current_identity
from flask_cors import CORS

import config
from auth import identity, authenticate
from healthify.utils import logger
from healthify.resources.auth import Singup, Signout, ForgotPassword

__author__ = 'rahul'

log = logger.logger

app = Flask(config.FLASK_APP_NAME)
app.config.from_object(config)
CORS(app)
api = Api(app)


JWT(app, authenticate, identity)


api.add_resource(Singup, '/signup')
api.add_resource(Signout, '/signout')
api.add_resource(ForgotPassword, '/password/forgot')

if __name__ == "__main__":
    app.run(debug=config.FLASK_DEBUG, port=config.FLASK_PORT)

