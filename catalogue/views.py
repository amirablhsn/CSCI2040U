from django.shortcuts import render
from .models import Vehicle
from django.db.models import Q, Value
from django.db.models.functions import Concat
from .forms import VehicleForm
from django.http import HttpResponseRedirect


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
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")
    else:
        form = VehicleForm
    return render(request, "add.html", {"form": form})