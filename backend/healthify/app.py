import json

from flask import Flask
from flask_jwt import JWT, jwt_required, current_identity
from flask_cors import CORS

import config
from auth import identity, authenticate
from healthify.utils import logger
from healthify import create_restful_api

__author__ = 'rahul'

log = logger.logger

app = Flask(config.FLASK_APP_NAME)
app.config.from_object(config)
# CORS(app)

create_restful_api(app)

JWT(app, authenticate, identity)


@app.route('/home', methods=['GET'])
def hello_world():
    log.info('This is a log message')
    return json.dumps(dict(message='Hello World!!'))


@app.route('/okay', methods=['GET'])
@jwt_required()
def okay():
    return current_identity.first_name

if __name__ == "__main__":
    app.run(debug=config.FLASK_DEBUG, port=config.FLASK_PORT)