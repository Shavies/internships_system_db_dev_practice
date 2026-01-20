from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Role, University


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "created_at")
    search_fields = ("name",)


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    search_fields = ("name",)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ("id",)

    # หน้า list: โชว์ให้ครบเท่าที่เหมาะ
    list_display = (
        "id",
        "phone_number",
        "email",
        "fname",
        "lname",
        "role",
        "university",
        "is_active",
        "is_staff",
        "is_superuser",
        "created_at",
        "updated_at",
        "last_login",
    )

    search_fields = ("phone_number", "email", "fname", "lname", "university__name", "role__name")
    list_filter = ("is_active", "is_staff", "is_superuser", "role", "university")
    autocomplete_fields = ("role", "university")

    readonly_fields = ("created_at", "updated_at", "last_login")

    # หน้า detail: จัดหมวดให้ครบทุก field ตาม models.py
    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        ("Personal info", {"fields": ("email", "fname", "lname", "role", "university")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Dates", {"fields": ("last_login", "created_at", "updated_at")}),
    )

    # หน้า add user ใน admin (สร้าง user ใหม่ใน admin)
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("phone_number", "password1", "password2"),
        }),
    )
