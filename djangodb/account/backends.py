from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from .models import Staff

User = get_user_model()

class PhoneBackend(BaseBackend):
    def authenticate(self, request, phone_number=None, password=None, **kwargs):
        if not phone_number or not password:
            return None
        try:
            user = User.objects.get(phone_number=str(phone_number).strip())
        except User.DoesNotExist:
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

    def user_can_authenticate(self, user):
        return getattr(user, "is_active", True)

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class EmployeeIdBackend(BaseBackend):
    def authenticate(self, request, employee_id=None, password=None, **kwargs):
        if not employee_id or not password:
            return None
        try:
            staff = Staff.objects.select_related("user").get(employee_id=str(employee_id).strip())
        except Staff.DoesNotExist:
            return None

        user = staff.user
        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

    def user_can_authenticate(self, user):
        return getattr(user, "is_active", True)

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
