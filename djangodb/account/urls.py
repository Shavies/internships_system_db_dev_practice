from django.urls import path
from .views import login_view, logout_view, home_view, register_owner_view, register_student_view

urlpatterns = [
    path("", home_view, name="home"),
    path("register/student/", register_student_view, name="register_student"),
    path("register/owner/", register_owner_view, name="register_owner"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]
