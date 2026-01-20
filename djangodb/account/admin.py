from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Role, University, Student, Department


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "created_at")
    search_fields = ("name",)


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    search_fields = ("name",)

@admin.register(Student)
class Student(admin.ModelAdmin):
    list_display = ("id", "user_id","mentor", "picture", "hours", "university", "start_date", "end_date", "major", "is_active")
    search_fields = ("user_id__phone_number",)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "dept_name", "created_at")
    search_fields = ("dept_name",)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ("id",)

    list_display = (
        "id",
        "phone_number",
        "email",
        "fname",
        "lname",
        "role",
        "department",   
        "is_active",
        "is_staff",
        "is_superuser",
        "created_at",
        "updated_at",
        "last_login",
    )

    search_fields = ("phone_number", "email", "fname", "lname", "role__name","department__name")
    list_filter = ("is_active", "is_staff", "is_superuser", "role")

    autocomplete_fields = ("role",) 

    readonly_fields = ("created_at", "updated_at", "last_login")

