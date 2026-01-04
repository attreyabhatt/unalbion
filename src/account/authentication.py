from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if request and request.path.startswith("/admin"):
            return None
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            return None
        if user.is_staff or user.is_superuser:
            return None
        # You can add additional checks here if needed
        return user
