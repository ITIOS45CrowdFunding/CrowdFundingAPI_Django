from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
User=get_user_model()
# handle email authentication
class EmailBackend(ModelBackend):
    # override to authenticate use my custom one
    def authenticate(self, request, email=None, password =None, **kwargs):
        try:
            user=User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None