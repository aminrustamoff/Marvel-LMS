from django.contrib.auth.backends import ModelBackend
from django.utils import timezone


class ActiveUntilModelBackend(ModelBackend):
    def user_can_authenticate(self, user):
        can_authenticate = super().user_can_authenticate(user)
        if not can_authenticate:
            return False

        active_until = getattr(user, "active_until", None)
        if active_until and active_until < timezone.localdate():
            return False

        return True