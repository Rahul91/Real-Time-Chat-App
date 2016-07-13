from flask_cors import CORS
from flask_restful import Api

from healthify.resources.auth import Singup, Signout
__author__ = 'rahul'


def create_restful_api(app):
    api = Api(app)

    CORS(app, resources={r"*": {"origins": "*"}})

    api.add_resource(Singup, '/signin')
    api.add_resource(Signout, '/signout')



