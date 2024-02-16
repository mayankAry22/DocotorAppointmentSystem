# middleware.py
from django.http import HttpResponseRedirect
from django.conf import settings
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exclude_urls = [reverse('login_user'), reverse('login_doctor'), 
                             reverse('register_user'), reverse('register_doctor'), 
                             reverse('admin:login'), reverse('admin:index'), reverse('index')]

    def __call__(self, request):
        if not request.user.is_authenticated and request.path_info not in self.exclude_urls:
            return HttpResponseRedirect(reverse(settings.LOGIN_REDIRECT_URL))
        response = self.get_response(request)
        return response