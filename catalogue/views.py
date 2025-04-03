from django.shortcuts import render, get_object_or_404
from .models import Vehicle
from .models import Favourite
from django.db.models import Q, Value
from django.db.models.functions import Concat
from .forms import VehicleForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required



# Create your views here.
def search(request):
    """Search the database for vehicles. Queries are matched based on make model and trim"""
    # Get query from the search bar input
    query = request.GET.get("catalogue-search", "")
    
    # The database to search through
    vehicles = Vehicle.objects.all()

    # Ensure that a query was recieved
    if query:
        # Combine make model and trim to search from, and get matches
        vehicles = vehicles.annotate(
            combined=Concat("make", Value(" "), "model", Value(" "), "trim")
        ).filter(combined__icontains=query)

    favourites = []
    if request.user.is_authenticated:
        # Get all the user's favourites, and get a list of vehicle ids
        favourites = Favourite.objects.filter(user=request.user).values_list("vehicle_id", flat=True)
    
    # Pagination: Show 16 vehicles per page
    paginator = Paginator(vehicles, 16)
    page_number = request.GET.get("page")
    vehicles_page = paginator.get_page(page_number)
    
    # Update the client with matches found and display them on the search page
    return render(request, "search.html", {"vehicles": vehicles_page, "query": query, "favourites": favourites})

def filter(request):
    """Filters vehicles based on request parameters."""
    vehicles = Vehicle.objects.all()

    # Get distinct values for dropdowns
    makes = Vehicle.objects.values_list("make", flat=True).distinct().order_by("make")
    models = Vehicle.objects.values_list("model", flat=True).distinct().order_by("model")
    years = Vehicle.objects.values_list("year", flat=True).distinct().order_by("-year")
    prices = Vehicle.objects.values_list("price", flat=True).distinct().order_by("price")

    # Get filter parameters from GET request
    make = request.GET.get("make", "")
    model = request.GET.get("model", "")
    year_min = request.GET.get("year_min", "")
    year_max = request.GET.get("year_max", "")
    price_min = request.GET.get("price_min", "")
    price_max = request.GET.get("price_max", "")

    # Apply filters
    if make:
        vehicles = vehicles.filter(make=make)
    if model:
        vehicles = vehicles.filter(model=model)
    if year_min:
        vehicles = vehicles.filter(year__gte=year_min)
    if year_max:
        vehicles = vehicles.filter(year__lte=year_max)
    if price_min:
        vehicles = vehicles.filter(price__gte=price_min)
    if price_max:
        vehicles = vehicles.filter(price__lte=price_max)

    # Pagination: Show 16 vehicles per page
    paginator = Paginator(vehicles, 16)
    page_number = request.GET.get("page")
    vehicles_page = paginator.get_page(page_number)

    return render(request, "filter.html", {
        "vehicles": vehicles_page,
        "makes": makes,
        "models": models,
        "years": years,
        "prices": prices
    })

def details(request, id):
    """Get the details of a specific vehicle and display them on the details page"""
    # Get the vehicle by ID, sends 404 if no vehicle with given id exist
    vehicle = get_object_or_404(Vehicle, id=id)
    
    # Check if vehicle entry has an image, if not display default image
    if vehicle.image:
        imageUrl = vehicle.image.url
    else:
        imageUrl = '/media/assets/sample2.png'

    # Send client to the details page with the details and image of the vehicle
    return render(request, "details.html", {"vehicle": vehicle, "imageUrl": imageUrl})


# Add, edit, delete functions require user to have staff privileges
@staff_member_required(login_url="/") #Redirect to home, if not admin
def add(request):
    """Adds a new vehicle to the database using details from the form"""
    if request.method == "POST":
        # Gets the form fields, and uploaded image file.
        form = VehicleForm(request.POST, request.FILES)

        # If valid, add the vehicle and redirect the client to the details of the newly added vehicle
        if form.is_valid():
            vehicle = form.save()
            return HttpResponseRedirect(reverse('details', args=[vehicle.id]))
    else:
        form = VehicleForm
    
    # Re-render the form page if the form was invalid
    return render(request, "add.html", {"form": form})

# function for editing an existing vehicle
@staff_member_required(login_url="/") #Redirect to home, if not admin
def edit(request, id):
    """Edits an existing vehicle in the database"""

    # Get the vehcile to edit by id
    vehicle = get_object_or_404(Vehicle, id=id)
    
    if request.method == "POST":
        # Get the new details/image for the vehicle from the form
        form = VehicleForm(request.POST, request.FILES, instance=vehicle)

        # If valid, update the vehicle in the database and redirect the client to the details page
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('details', args=[vehicle.id]))
    else:
        form = VehicleForm(instance=vehicle)

    # Re-render edit page if invalid form
    return render(request, "edit.html", {"form": form, "vehicle": vehicle})

# function to delete an existing vehicle
@staff_member_required(login_url="/") #Redirect to home, if not admin
def delete(request, id):
    """Deletes a vehicle from the database"""
    vehicle= get_object_or_404(Vehicle, id=id)
    if request.method == "POST":
        # Deletes the vehicle and notifies the client that it was deleted
        vehicle.delete()
        messages.success(request, f'"{vehicle.make} {vehicle.model}" has been deleted from the catalogue.')
        return redirect("/")
    # If a POST request was not sent, re-render the vehicle's detail page
    return render(request, "details.html", {"vehicle": vehicle})

@login_required(login_url="/users/login") #Redirect to login in not logged in
def toggle_favourite(request, id):
    """Adds or remove vehicle from user's favourites list"""
    vehicle = get_object_or_404(Vehicle, id=id)

    # Tries to fetch, if database entry doesnt exist create new favourite
    favourite, isCreated = Favourite.objects.get_or_create(user=request.user, vehicle=vehicle)
    if not isCreated:
        # Already favourited, so remove
        favourite.delete()

    # Returns to same page
    return redirect(request.META.get("HTTP_REFERER", ""))
