from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm, RegisterForm
from django.contrib.auth.decorators import login_required
from catalogue.models import Favourite
from django.core.paginator import Paginator


# Create your views here.
def register(request):
    """Register a new user from form input"""
    if request.method == "POST":
        form = RegisterForm(request.POST)

        # Save the new user and log them in if form is valid
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Successfully registered and logged in!")
            return redirect("/")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})

def login_view(request):
    """Login user from username/password form input"""
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)
        # Get inputted username and passowrd and authenticate
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            # If username/password are correct login user
            if user is not None:
                login(request, user)
                messages.success(request, "Successfully logged in.")
                return redirect("/")
            else:
                messages.error(request, "Invalid username or password.")

    return render(request, "login.html", {"form": form})

def logout_view(request):
    """Logs out user"""
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("/")
    
# Requires logged in user  to view profile, redirects to login in page if not
@login_required(login_url="/users/login")
def profile_view(request):
    """Display the users profile page with their favourite vehicles"""
    # Get all favourites (objects)
    user_favourites = Favourite.objects.filter(user=request.user).select_related("vehicle")
    favourites = []
    ids = []
    # parse through all faviouties and creates list of favouited vehicles and their ids
    for entry in user_favourites:
        favourites.append(entry.vehicle)
        ids.append(entry.vehicle.id)


    # Pagination: Show 16 vehicles per page
    paginator = Paginator(favourites, 16)
    page_number = request.GET.get("page")
    favourites_page = paginator.get_page(page_number)


    # Send favourites to user profile page for display
    return render(request, "profile.html", {"favourites": favourites_page,  "ids": ids})

@login_required(login_url="/users/login")
def request_admin(request):
    """Sets user to admin on request"""
    if request.method == "POST":
        # Set user to staff
        request.user.is_staff = True
        request.user.save()
        messages.success(request, "You are now an admin")
    return redirect("profile")

@login_required(login_url="/users/login")
def remove_admin(request):
    """Removes admin from user"""
    if request.method == "POST":
        # Remove staff
        request.user.is_staff = False
        request.user.save()
        messages.success(request, "Your admin role has been removed")
    return redirect("profile")