from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, StudentRegisterForm, OwnerRegisterForm

BACKEND_PATH = "account.backends.PhoneBackend"

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


def register_student_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = StudentRegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()

        # authenticate ก่อน login 
        raw_password = form.cleaned_data["password1"]
        authed_user = authenticate(
            request,
            phone_number=user.phone_number,
            password=raw_password,
        )
        if authed_user is not None:
            login(request, authed_user)
        return redirect("home")

    return render(request, "account/register_student.html", {"form": form})


def register_owner_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = OwnerRegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()

        # authenticate ก่อน login 
        raw_password = form.cleaned_data["password1"]
        authed_user = authenticate(
            request,
            phone_number=user.phone_number,
            password=raw_password,
        )
        if authed_user is not None:
            login(request, authed_user)
        return redirect("home")

    return render(request, "account/register_owner.html", {"form": form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["user"]

            login(request, user, backend=BACKEND_PATH)
            return redirect("home")
    else:
        form = LoginForm()

    return render(request, "account/login.html", {"form": form})

def logout_view(request):  
    logout(request)
    return redirect("login")

@login_required
def home_view(request):
    role_name = request.user.role.name if request.user.role else "UNKNOWN"
    return render(request, "account/home.html", {"role_name": role_name})
