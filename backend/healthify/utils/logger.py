import logging
from logging.config import dictConfig

from healthify.config import LOGGING_CONFIG, DEFAULT_LOGGER_NAME

__author__ = 'rahul'


def get_logger(logger_name=None):
    dictConfig(LOGGING_CONFIG)
    return logging.getLogger(logger_name or DEFAULT_LOGGER_NAME)

