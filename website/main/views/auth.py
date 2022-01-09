"""Views to login/logout."""
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# from django.views.decorators.cache import never_cache

from django.views import View
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    """Login a user if the credentials are ok."""

    def get(self, request, *args, **kwargs):
        """Getter."""
        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        """Try to login with the requested credentials."""
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return HttpResponseRedirect('/workouts/')
        else:
            return HttpResponseRedirect('/login/')


class LogoutView(View):
    """View to logout a user."""

    def get(self, request):
        """."""
        logout(request)
        return HttpResponseRedirect('/login/')
