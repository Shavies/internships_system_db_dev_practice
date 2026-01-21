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
        user.set_password(password)
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

        from .models import Role  
        admin_role, _ = Role.objects.get_or_create(
            name="ADMIN",
            defaults={"description": "System Administrator"},
        )
        extra_fields["role"] = admin_role

        return self.create_user(phone_number, password, **extra_fields)
    
    def save(self, *args, **kwargs):
        if self.is_superuser and self.role and self.role.name != "ADMIN":
            raise ValueError("Superuser must have ADMIN role")
        super().save(*args, **kwargs)

class Department(models.Model):
    dept_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    def __str__(self):
        return self.dept_name

class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    
    def __str__(self):
        return self.name

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(blank=True, null=True, unique=True)
    phone_number = models.CharField(max_length=20, unique=True)

    role = models.ForeignKey(
        'Role',
        related_name='users',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    department = models.ForeignKey(
        'Department',
        related_name='users',
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
    
    fname = models.CharField(max_length=100, blank=True)
    lname = models.CharField(max_length=100, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []  # createsuperuser required

    def __str__(self):
        return self.phone_number

class University(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.name
    
class Staff(models.Model):
    user = models.OneToOneField(
        'User',
        related_name='staff_profile',
        on_delete=models.PROTECT,
        null=False,
        blank=False
    )
    employee_id = models.CharField(max_length=50, unique=True) 
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        if self.user:
            return f"Staff: {self.user.phone_number}"
        return f"Staff #{self.id}"

class Major(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(
        'User',
        related_name='student_profile',
        on_delete=models.PROTECT,
        null=False,
        blank=False
    )


    mentor = models.ForeignKey(
        'Staff',
        related_name='students',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    picture = models.CharField(max_length=255, blank=True, null= True)
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    university = models.ForeignKey(
        'University',
        related_name='students',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    major = models.ForeignKey(
        'Major',
        related_name='students',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    
    is_active = models.BooleanField(default=True)

    def __str__(self):
        if self.user:
            return f"Student: {self.user.phone_number}"
        return f"Student #{self.id}"





        