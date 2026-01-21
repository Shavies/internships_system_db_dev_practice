from django.urls import path
from .views import (
    home_view,
    login_student_view, login_owner_view,
    register_student_view, register_owner_view,
    logout_view
)

urlpatterns = [
    path("", home_view, name="home"),

    path("login/student/", login_student_view, name="login_student"),
    path("login/owner/", login_owner_view, name="login_owner"),

    path("register/student/", register_student_view, name="register_student"),
    path("register/owner/", register_owner_view, name="register_owner"),

    path("logout/", logout_view, name="logout"),
]
