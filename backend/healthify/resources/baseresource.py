from flask import request
from flask_restful import Resource
from flask_restful.utils import unpack, OrderedDict
from werkzeug.wrappers import Response as ResponseBase

# from healthify.config import
from healthify.utils import logger

log = logger.logger
# CONFIG = get_config()
# increment = CONFIG.statsd.incr
# total_requests = CONFIG.total_requests


class BaseResource(Resource):
    def __init__(self, *args, **kwargs):
        super(Resource, self).__init__(*args, **kwargs)

    def dispatch_request(self, *args, **kwargs):
        # Taken from flask

        meth = getattr(self, request.method.lower(), None)
        if meth is None and request.method == 'HEAD':
            meth = getattr(self, 'get', None)
        assert meth is not None, 'Unimplemented method %r' % request.method

        for decorator in self.method_decorators:
            meth = decorator(meth)

        # try:
        #     increment(total_requests)
        # except Exception as exc:
        #     log.error('statd failed {} : Request full path : {}'.format(
        #         exc.message, request.full_path))

        # this is where actual method starts
        log.debug('{} Method Starts {}'.format(
            request.method, request.full_path))
        resp = meth(*args, **kwargs)
        log.debug('{} Method Ends {}'.format(
            request.method, request.full_path))
        # this is where actual method ends

        if isinstance(resp, ResponseBase):  # There may be a better way to test
            return resp

        representations = self.representations or OrderedDict()

        mediatype = request.accept_mimetypes.best_match(representations,
                                                        default=None)
        if mediatype in representations:
            data, code, headers = unpack(resp)
            resp = representations[mediatype](data, code, headers)
            resp.headers['Content-Type'] = mediatype
            return resp

        return resp
