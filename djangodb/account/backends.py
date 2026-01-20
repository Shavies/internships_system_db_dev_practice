from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class PhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, phone_number=None, **kwargs):
        # Admin/Django AuthenticationForm จะส่งมาเป็น username
        login_id = phone_number or username or kwargs.get(User.USERNAME_FIELD)

        if not login_id or not password:
            return None

        login_id = str(login_id).strip()

        try:
            user = User.objects.get(phone_number=login_id)
        except User.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
