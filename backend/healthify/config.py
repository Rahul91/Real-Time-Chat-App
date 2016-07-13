import os
from datetime import timedelta

__author__ = 'rahul'

basedir = os.path.abspath(os.path.dirname(__file__))

# Flask #
FLASK_APP_NAME = "healhify"
FLASK_DEBUG = True
ERROR_404_HELP = False
FLASK_PORT = 3434

# SQLAlchemy #
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'healthify.db')
SQLALCHEMY_DATABASE_URI = 'postgresql://rahul:root@localhost:5433/healthify'
# SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:root@localhost/healthify'
SQLALCHEMY_ECHO = True
SQLALCHEMY_POOL_CYCLE = 3600
SQLALCHEMY_CONVERT_UNICODE = True

# Flask JWT #
SECRET_KEY = '\x8c\x1eW\xcd\x07\x87\x82\xef4M\xdc;\x81u\x8c \xe3\x06d\xda\xb6{\xa3\xb2'  # Mandatory
JWT_EXPIRATION_DELTA = timedelta(hours=8)

# Logging Conf #
LOGGING_CONFIG = dict(
    version=1,
    formatters={
        'compact': {'format':
                        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'},
        'verbose': {
            'format': '%(asctime)s [%(levelname)-8.8s] %(name)-8.8s [%(filename)-15.15s:%(lineno)-3.3s]: %(message)s'
        }
    },
    handlers={
        'default': {'class': 'logging.StreamHandler',
                    'formatter': 'compact',
                    'level': 'DEBUG'
                    },
        'api': {'class': 'logging.FileHandler',
                'formatter': 'compact',
                'filename': '%s/%s' % (basedir, '../logs/api/api.log'),
                'level': 'DEBUG'
                },
    },
    loggers={
        '': {
            'handlers': ['api'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
)
