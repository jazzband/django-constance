import datetime

from django.core.handlers.wsgi import WSGIRequest



class FakeRequest(WSGIRequest):

    def __init__(self, user=None, meta=None, environ=None, cookies=None):
        if not environ:
            environ = {
                'PATH_INFO':         '/',
                'QUERY_STRING':      '',
                'REMOTE_ADDR':       '127.0.0.1',
                'REQUEST_METHOD':    'GET',
                'SCRIPT_NAME':       '',
                'SERVER_NAME':       'testserver',
                'SERVER_PORT':       '80',
                'SERVER_PROTOCOL':   'HTTP/1.1',
                'wsgi.version':      (1,0),
                'wsgi.url_scheme':   'http',
                'wsgi.errors':       [],
                'wsgi.multiprocess': True,
                'wsgi.multithread':  False,
                'wsgi.run_once':     False,
                'wsgi.input':        None,
            }
        super(FakeRequest, self).__init__(environ)
        if user:
            self.user = user
        if meta:
            self.META.update(meta)
        if cookies:
            self.COOKIES.update(cookies)
        self.xnow = datetime.datetime.now()

    @classmethod
    def from_test_response(cls, response, *args, **kwargs):
        return cls(environ=response.request, *args, **kwargs)


