from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("phone_number is required")

        phone_number = str(phone_number).strip()
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)  # Django hashing
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(blank=True, null=True, unique=True)
    phone_number = models.CharField(max_length=20, unique=True)

    role = models.ForeignKey(
        'Role',
        related_name='users',
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    fname = models.CharField(max_length=100, blank=True)
    lname = models.CharField(max_length=100, blank=True)

    university = models.ForeignKey(
        'University',
        related_name='users',
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []  # createsuperuser -> phone_number + password

    def __str__(self):
        return self.phone_number
    
class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    
    def __str__(self):
        return self.name

class University(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.name

    