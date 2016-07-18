from healthify import config
from healthify.app import app

__author__ = 'rahul'

if __name__ == "__main__":
    app.run(debug=config.FLASK_DEBUG, port=config.FLASK_PORT)
