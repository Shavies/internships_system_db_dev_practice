from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, LoginForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='account.backends.PhoneBackend')
            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "account/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["user"]
            login(request, user, backend='account.backends.PhoneBackend')
            return redirect("home")
    else:
        form = LoginForm()

    return render(request, "account/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def home_view(request):
    return render(request, "account/home.html")
