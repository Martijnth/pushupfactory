
from django.urls.base import resolve

from django.http.response import HttpResponseRedirect


class AuthRequiredMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        url = resolve(request.path)

        # we need to get the person (and set the language) right at the start
        if request.user.is_authenticated or url.url_name == 'login':

            if request.user.is_anonymous:
                response = self.get_response(request)
                return response

            response = self.get_response(request)
            return response
        print('Why?', request.user)
        return HttpResponseRedirect('/login/')
