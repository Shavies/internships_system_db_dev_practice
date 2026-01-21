from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .forms import StudentLoginForm, OwnerLoginForm, StudentRegisterForm, OwnerRegisterForm

BACKEND_PHONE_PATH = "account.backends.PhoneBackend"
BACKEND_EMPLOYEE_PATH= "account.backends.EmployeeIdBackend"

#from .forms import BaseRegisterForm
# def register_view(request):
#     if request.user.is_authenticated:
#         return redirect("home")

#     if request.method == "POST":
#         form = BaseRegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user, backend='account.backends.PhoneBackend')
#             return redirect("home")
#     else:
#         form = BaseRegisterForm()

#     return render(request, "account/register.html", {"form": form})


def login_student_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = StudentLoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.cleaned_data["user"]
        login(request, user, backend=BACKEND_PHONE_PATH)
        return redirect("home")

    return render(request, "account/login_student.html", {"form": form})


def login_owner_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = OwnerLoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.cleaned_data["user"]
        login(request, user, backend=BACKEND_EMPLOYEE_PATH)
        return redirect("home")

    return render(request, "account/login_owner.html", {"form": form})


def register_student_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = StudentRegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        # student -> login ด้วย PhoneBackend
        login(request, user, backend="account.backends.PhoneBackend")
        return redirect("home")

    return render(request, "account/register_student.html", {"form": form})


def register_owner_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = OwnerRegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        # owner -> login ด้วย EmployeeIdBackend
        login(request, user, backend="account.backends.EmployeeIdBackend")
        return redirect("home")

    return render(request, "account/register_owner.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login_student")  


@login_required
def home_view(request):
    role_name = request.user.role.name if request.user.role else "UNKNOWN"
    return render(request, "account/home.html", {"role_name": role_name})
