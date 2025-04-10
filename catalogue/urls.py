from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.search, name="search"),
    path("filter/", views.filter, name="filter"),
    path("add/", views.add, name="add"),
    path("vehicle/<int:id>/", views.details, name="details"),
    path('edit/<int:id>/', views.edit, name='edit'),
    path("delete/<int:id>/", views.delete, name="delete"),
    path("favourite/<int:id>/", views.toggle_favourite, name="toggle_favourite"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)