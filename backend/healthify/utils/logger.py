import logging
from logging.config import dictConfig

from healthify.config import LOGGING_CONFIG

__author__ = 'rahul'


dictConfig(LOGGING_CONFIG)
logger = logging.getLogger()
