from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

Farmer = get_user_model()

class EmailOrUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None

        try:
            user = Farmer.objects.get(
                Q(username=username) | Q(email=username)
            )
        except Farmer.DoesNotExist:
            return None

        if user.check_password(password) and user.is_active:
            return user
        return None
