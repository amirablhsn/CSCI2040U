from django.urls import path
from . import views

urlpatterns = [
    path("", views.search, name="search"),
    path("add/", views.add, name="add"),
]