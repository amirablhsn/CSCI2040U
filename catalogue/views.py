from django.shortcuts import render, get_object_or_404, redirect
from .models import Vehicle
from django.db.models import Q, Value
from django.db.models.functions import Concat
from .forms import VehicleForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages


# Create your views here.
def search(request):
    query = request.GET.get("catalogue-search", "")
    vehicles = []
    if query:
        vehicles = Vehicle.objects.annotate(
            combined=Concat("make", Value(" "), "model", Value(" "), "trim")
            ).filter(combined__icontains=query)


    return render(request, "search.html", {"vehicles" : vehicles, "query" : query})

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

def delete(request, id):
    vehicle= get_object_or_404(Vehicle, id=id)
    if request.method == "POST":
        vehicle.delete()
        messages.success(request, f'"{vehicle.make} {vehicle.model}" has been deleted from the catalogue.')
        return redirect("/")
    return render(request, "details.html", {"vehicle": vehicle})