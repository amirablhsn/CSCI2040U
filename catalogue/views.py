from django.shortcuts import render
from .models import Vehicle

# Create your views here.
def search(request):
    query = request.GET.get("catalogue-search", "")
    vehicles = []
    if query:
        vehicles = Vehicle.objects.filter(name__icontains=query)

    return render(request, "search.html", {"vehicles" : vehicles, "query" : query})
