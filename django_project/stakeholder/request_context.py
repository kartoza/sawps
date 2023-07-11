import threading

_request_context = threading.local()

def set_request(request):
    _request_context.request = request

def get_request():
    return getattr(_request_context, 'request', None)
