from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from .models import Staff

User = get_user_model()


class PhoneBackend(BaseBackend):
    def authenticate(self, request, phone_number=None, password=None, **kwargs):
        if not phone_number or not password:
            return None

        phone_number = str(phone_number).strip()
        try:
            user = User.objects.get(phone_number=phone_number)
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
    # backend auth เฉพาะ employee_id 
    def authenticate(self, request, employee_id=None, password=None, **kwargs):
        if not employee_id or not password:
            return None

        employee_id = str(employee_id).strip()
        try:
            staff = Staff.objects.select_related("user").get(employee_id=employee_id)
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


class OwnerBackend(BaseBackend):
    """
    OWNER login แบบรวม:
    - ถ้าใส่ employee_id: หาใน Staff.employee_id
    - ถ้าไม่เจอ: ลองเป็น phone_number (admin)
    - อนุญาตเฉพาะ user ที่ role=OWNER หรือ is_staff=True
    """
    def authenticate(self, request, identifier=None, password=None, **kwargs):
        if not identifier or not password:
            return None

        identifier = str(identifier).strip()
        user = None

        # 1) ลอง employee_id ผ่าน Staff
        try:
            staff = Staff.objects.select_related("user").get(employee_id=identifier)
            user = staff.user
        except Staff.DoesNotExist:
            pass

        # 2) ถ้าไม่เจอ ลอง phone_number (กรณี admin)
        if user is None:
            try:
                user = User.objects.get(phone_number=identifier)
            except User.DoesNotExist:
                return None

        # 3) ตรวจ password + active
        if not user.check_password(password) or not self.user_can_authenticate(user):
            return None

        # 4) ตรวจสิทธิ์เข้า OWNER page
        role_name = getattr(getattr(user, "role", None), "name", None)
        if user.is_staff or role_name == "OWNER":
            return user

        return None

    def user_can_authenticate(self, user):
        return getattr(user, "is_active", True)

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
