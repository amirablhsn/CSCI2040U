from django.shortcuts import render, get_object_or_404
from .models import Vehicle
from django.db.models import Q, Value
from django.db.models.functions import Concat
from .forms import VehicleForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect

# Create your views here.
def search(request):
    query = request.GET.get("catalogue-search", "")
    vehicles = []
    if query:
        vehicles = Vehicle.objects.annotate(
            combined=Concat("make", Value(" "), "model", Value(" "), "trim")
            ).filter(combined__icontains=query)


    return render(request, "search.html", {"vehicles" : vehicles, "query" : query})

def filter(request):
    """Filters vehicles based on request parameters."""
    vehicles = Vehicle.objects.all()

    # Get distinct values for dropdowns
    makes = Vehicle.objects.values_list("make", flat=True).distinct().order_by("make")
    models = Vehicle.objects.values_list("model", flat=True).distinct().order_by("model")
    years = Vehicle.objects.values_list("year", flat=True).distinct().order_by("-year")  # Sorted from newest to oldest
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

    return render(request, "filter.html", {
        "vehicles": vehicles,
        "makes": makes,
        "models": models,
        "years": years,
        "prices": prices
    })



# https://docs.djangoproject.com/en/5.1/topics/forms/
def add(request):
    if request.method == "POST":
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            vehicle = form.save()
            return HttpResponseRedirect(reverse('details', args=[vehicle.id]))
    else:
        form = VehicleForm
    return render(request, "add.html", {"form": form})

def details(request, id):
    vehicle = get_object_or_404(Vehicle, id=id)
    if vehicle.image:
        imageUrl = vehicle.image.url
    else:
        imageUrl = '/media/assets/sample3.png'
    return render(request, "details.html", {"vehicle": vehicle, "imageUrl": imageUrl})

# function for editing an existing vehicle
def edit(request, id):
    vehicle = get_object_or_404(Vehicle, id=id)
    
    if request.method == "POST":
        form = VehicleForm(request.POST, request.FILES, instance=vehicle)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('details', args=[vehicle.id]))
    else:
        form = VehicleForm(instance=vehicle)

    return render(request, "edit.html", {"form": form, "vehicle": vehicle})

# function to delete an existing vehicle
def delete(request, id):
    vehicle= get_object_or_404(Vehicle, id=id)
    if request.method == "POST":
        vehicle.delete()
        messages.success(request, f'"{vehicle.make} {vehicle.model}" has been deleted from the catalogue.')
        return redirect("/")
    return render(request, "details.html", {"vehicle": vehicle})