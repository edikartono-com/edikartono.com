from django.utils.decorators import sync_and_async_middleware
from threading import current_thread

_REQUESTS = {}

class RequestNotFound(Exception):
    def __init__(self, message):
        self.message = message

def get_request():
    thread = current_thread()
    if thread not in _REQUESTS:
        raise RequestNotFound('global request errors')
    else:
        return _REQUESTS[thread]

class IntroMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
    
    def process_request(self, request):
        xxx =  _REQUESTS[current_thread()] = request
        return xxx
    
    @sync_and_async_middleware
    def __call__(self, request):
        from corecode.models import Intro
        self.process_request(request)
        intros = Intro.objects.last()
        if intros:
            request.intro = intros
        response = self.get_response(request)
        return response