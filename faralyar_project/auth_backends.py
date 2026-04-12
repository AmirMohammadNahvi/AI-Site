from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from accounts.models import User


class EmailOrMobileBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        identifier = username or kwargs.get("email") or kwargs.get("mobile")
        if not identifier or not password:
            return None
        try:
            user = User.objects.get(Q(email__iexact=identifier) | Q(mobile=identifier))
        except User.DoesNotExist:
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
