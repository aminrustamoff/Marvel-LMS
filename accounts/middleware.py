from django.contrib.auth import logout
from django.utils import timezone


class ActiveUntilMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)
        if user and user.is_authenticated:
            active_until = getattr(user, "active_until", None)
            if active_until and active_until < timezone.localdate():
                logout(request)

        return self.get_response(request)