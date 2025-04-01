from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm, RegisterForm
from django.contrib.auth.decorators import login_required


# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Successfully registered and logged in!")
            return redirect("/")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})

def login_view(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Successfully logged in.")
                return redirect("/")
            else:
                messages.error(request, "Invalid username or password.")

    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("/")
    
@login_required
def profile_view(request):
    return render(request, "profile.html")

@login_required
def request_admin(request):
    if request.method == "POST":
        request.user.is_staff = True
        request.user.save()
        messages.success(request, "You are now an admin")
    return redirect("profile")

@login_required
def remove_admin(request):
    if request.method == "POST":
        request.user.is_staff = False
        request.user.save()
        messages.success(request, "Your admin role has been removed")
    return redirect("profile")